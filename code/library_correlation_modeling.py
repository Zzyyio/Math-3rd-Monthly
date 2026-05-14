"""Library circulation analytics pipeline.

Tasks covered:
1) Extract book-level features from circulation records and summary data.
2) Compute multiple association matrices (Pearson/Spearman/Kendall/Mutual Information).
3) Train predictive models (Random Forest + XGBoost if available) for:
   - 总借入和续借量
   - 平均借阅时间(天)
4) Analyze features of popular books.

Run:
    python code/library_correlation_modeling.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import mutual_info_regression
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "dataset"
OUTPUT_DIR = ROOT / "output_dataset" / "analysis_outputs"

ALL_XLSX = DATASET_DIR / "all.xlsx"
SUMMARY_CSV = DATASET_DIR / "汇总结果.csv"


@dataclass
class ModelResult:
    target: str
    model_name: str
    mae: float
    r2: float
    top_features: List[Tuple[str, float]]


def _to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce")


def _to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    all_df = pd.read_excel(ALL_XLSX)
    summary_df = pd.read_csv(SUMMARY_CSV, encoding="utf-8-sig")
    return all_df, summary_df


def build_book_level_features(all_df: pd.DataFrame, summary_df: pd.DataFrame) -> pd.DataFrame:
    df = all_df.copy()
    df["Circulation Time"] = _to_datetime(df["Circulation Time"])
    df["Price"] = _to_numeric(df["Price"])
    df["Pages"] = _to_numeric(df["Pages"])

    # Event flags and times
    is_borrow = df["Circulation Type"].astype(str).str.contains("借", na=False)
    is_renew = df["Circulation Type"].astype(str).str.contains("续", na=False)
    is_return = df["Circulation Type"].astype(str).str.contains("归还", na=False)

    grp = df.groupby("Title", dropna=False)

    features = grp.agg(
        record_count=("Title", "size"),
        unique_users=("UserID", "nunique"),
        unique_grades=("Grade", "nunique"),
        median_price=("Price", "median"),
        median_pages=("Pages", "median"),
        first_circulation=("Circulation Time", "min"),
        last_circulation=("Circulation Time", "max"),
        place_mode=("Place of Publication", lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan),
        publisher_mode=("Publisher", lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan),
        author_mode=("Author", lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan),
        classnum_mode=("Classification Number", lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan),
    ).reset_index()

    borrow_count = grp.apply(lambda g: int(is_borrow.loc[g.index].sum())).rename("borrow_count")
    renew_count = grp.apply(lambda g: int(is_renew.loc[g.index].sum())).rename("renew_count")
    return_count = grp.apply(lambda g: int(is_return.loc[g.index].sum())).rename("return_count")

    features = features.merge(borrow_count.reset_index(), on="Title", how="left")
    features = features.merge(renew_count.reset_index(), on="Title", how="left")
    features = features.merge(return_count.reset_index(), on="Title", how="left")

    features["active_days"] = (features["last_circulation"] - features["first_circulation"]).dt.days
    features["borrow_per_user"] = features["borrow_count"] / features["unique_users"].replace(0, np.nan)

    summary = summary_df.copy()
    summary["Price"] = _to_numeric(summary["Price"])
    summary["Pages"] = _to_numeric(summary["Pages"])
    summary["总借入和续借量"] = _to_numeric(summary["总借入和续借量"])
    summary["平均借阅时间(天)"] = _to_numeric(summary["平均借阅时间(天)"])

    merged = summary.merge(features, on="Title", how="left", suffixes=("_summary", "_events"))

    # normalized year features
    merged["publication_year"] = _to_datetime(merged["Publication time"]).dt.year
    merged["book_age"] = pd.Timestamp.today().year - merged["publication_year"]

    return merged


def compute_associations(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    num_df = df[numeric_cols].copy()

    pearson = num_df.corr(method="pearson")
    spearman = num_df.corr(method="spearman")
    kendall = num_df.corr(method="kendall")

    # Mutual information matrix (target-wise for each numeric variable)
    mi_matrix = pd.DataFrame(index=numeric_cols, columns=numeric_cols, dtype=float)
    for target in numeric_cols:
        y = num_df[target]
        X = num_df.drop(columns=[target])
        valid = y.notna() & X.notna().all(axis=1)
        if valid.sum() < 20:
            mi_matrix.loc[target, :] = np.nan
            continue
        mi = mutual_info_regression(X.loc[valid], y.loc[valid], random_state=42)
        mi_series = pd.Series(mi, index=X.columns)
        mi_matrix.loc[target, target] = np.nan
        for c in X.columns:
            mi_matrix.loc[target, c] = mi_series[c]

    return {
        "pearson": pearson,
        "spearman": spearman,
        "kendall": kendall,
        "mutual_info": mi_matrix,
    }


def _build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = [c for c in X.columns if c not in numeric_features]

    numeric_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )
    categorical_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, numeric_features),
            ("cat", categorical_pipe, categorical_features),
        ]
    )


def _extract_top_features(pipeline: Pipeline, top_k: int = 20) -> List[Tuple[str, float]]:
    model = pipeline.named_steps["model"]
    pre = pipeline.named_steps["preprocessor"]
    feature_names = pre.get_feature_names_out()
    importances = model.feature_importances_
    idx = np.argsort(importances)[::-1][:top_k]
    return [(str(feature_names[i]), float(importances[i])) for i in idx]


def train_models(df: pd.DataFrame, targets: List[str]) -> List[ModelResult]:
    drop_columns = ["Title", "ISBN", "Author", "Classification Number"]
    target_set = set(targets)
    X = df.drop(columns=[c for c in drop_columns if c in df.columns] + [t for t in targets if t in df.columns], errors="ignore")

    results: List[ModelResult] = []

    for target in targets:
        y = _to_numeric(df[target])
        valid = y.notna()
        Xv = X.loc[valid].copy()
        yv = y.loc[valid].copy()

        X_train, X_test, y_train, y_test = train_test_split(Xv, yv, test_size=0.2, random_state=42)

        preprocessor = _build_preprocessor(X_train)

        rf = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", RandomForestRegressor(n_estimators=400, random_state=42, n_jobs=-1)),
            ]
        )
        rf.fit(X_train, y_train)
        pred = rf.predict(X_test)
        results.append(
            ModelResult(
                target=target,
                model_name="RandomForestRegressor",
                mae=mean_absolute_error(y_test, pred),
                r2=r2_score(y_test, pred),
                top_features=_extract_top_features(rf, top_k=20),
            )
        )

        # XGBoost optional fallback
        try:
            from xgboost import XGBRegressor  # type: ignore

            xgb = Pipeline(
                steps=[
                    ("preprocessor", preprocessor),
                    (
                        "model",
                        XGBRegressor(
                            n_estimators=500,
                            learning_rate=0.05,
                            max_depth=6,
                            subsample=0.9,
                            colsample_bytree=0.9,
                            random_state=42,
                            objective="reg:squarederror",
                            n_jobs=-1,
                        ),
                    ),
                ]
            )
            xgb.fit(X_train, y_train)
            pred_xgb = xgb.predict(X_test)
            results.append(
                ModelResult(
                    target=target,
                    model_name="XGBRegressor",
                    mae=mean_absolute_error(y_test, pred_xgb),
                    r2=r2_score(y_test, pred_xgb),
                    top_features=_extract_top_features(xgb, top_k=20),
                )
            )
        except Exception:
            pass

    return results


def analyze_popular_books(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["总借入和续借量"] = _to_numeric(work["总借入和续借量"])
    threshold = work["总借入和续借量"].quantile(0.8)
    work["is_popular"] = work["总借入和续借量"] >= threshold

    numeric_cols = work.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c != "is_popular"]

    pop = work[work["is_popular"]]
    non_pop = work[~work["is_popular"]]

    rows = []
    for c in numeric_cols:
        p_mean = pop[c].mean()
        np_mean = non_pop[c].mean()
        diff = p_mean - np_mean
        lift = (p_mean / np_mean) if pd.notna(np_mean) and np_mean != 0 else np.nan
        rows.append({"feature": c, "popular_mean": p_mean, "non_popular_mean": np_mean, "diff": diff, "lift": lift})

    result = pd.DataFrame(rows).sort_values("diff", key=lambda s: s.abs(), ascending=False)
    return result


def save_outputs(feature_df: pd.DataFrame, associations: Dict[str, pd.DataFrame], model_results: List[ModelResult], popular_df: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    feature_df.to_csv(OUTPUT_DIR / "book_level_features.csv", index=False, encoding="utf-8-sig")

    for name, mat in associations.items():
        mat.to_csv(OUTPUT_DIR / f"association_{name}.csv", encoding="utf-8-sig")

    mr_rows = []
    tf_rows = []
    for r in model_results:
        mr_rows.append({"target": r.target, "model": r.model_name, "mae": r.mae, "r2": r.r2})
        for rank, (fname, imp) in enumerate(r.top_features, start=1):
            tf_rows.append({"target": r.target, "model": r.model_name, "rank": rank, "feature": fname, "importance": imp})

    pd.DataFrame(mr_rows).to_csv(OUTPUT_DIR / "model_metrics.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(tf_rows).to_csv(OUTPUT_DIR / "model_top_features.csv", index=False, encoding="utf-8-sig")

    popular_df.to_csv(OUTPUT_DIR / "popular_book_feature_profile.csv", index=False, encoding="utf-8-sig")


def main() -> None:
    all_df, summary_df = load_data()
    feature_df = build_book_level_features(all_df, summary_df)
    associations = compute_associations(feature_df)
    targets = ["总借入和续借量", "平均借阅时间(天)"]
    model_results = train_models(feature_df, targets)
    popular_df = analyze_popular_books(feature_df)
    save_outputs(feature_df, associations, model_results, popular_df)
    print(f"Done. Outputs saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
