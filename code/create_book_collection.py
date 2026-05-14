import pandas as pd
import numpy as np

# ---------- 读取 ----------
df = pd.read_excel('/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/all_g12.xlsx')
df.columns = [c.strip() for c in df.columns]
df['Circulation Time'] = pd.to_datetime(df['Circulation Time'])

# ---------- 计算每个馆藏条码的指标 ----------
records = []
for barcode, grp in df.groupby('Collection Barcode'):
    grp = grp.sort_values('Circulation Time')
    events = grp[['Circulation Type', 'Circulation Time']].values

    borrows = 0
    renewals = 0
    current_start = None
    durations = []

    for ctype, ctime in events:
        if ctype == '外借':
            borrows += 1
            current_start = ctime
        elif ctype == '续借':
            renewals += 1
        elif ctype == '归还':
            if current_start is not None:
                days = (ctime - current_start).total_seconds() / 86400.0
                if days >= 0:
                    durations.append(days)
                current_start = None

    records.append({
        'Collection Barcode': barcode,
        '总借入': borrows,
        '总续借': renewals,
        '总借入和续借量': borrows + renewals,
        '已归还次数': len(durations),
        '总借阅时长': sum(durations)   # 用于后续加权平均
    })

bc_df = pd.DataFrame(records)

# ---------- 书目信息去重 ----------
meta_cols = ['Title', 'ISBN', 'Price', 'Author', 'Publisher',
             'Publication time', 'Place of Publication', 'Pages', 'Classification Number']
book_meta = df[['Collection Barcode'] + meta_cols].drop_duplicates(subset='Collection Barcode')

# ---------- 合并 ----------
full = book_meta.merge(bc_df, on='Collection Barcode', how='left')

# ---------- 按 Title 聚合 ----------
title_agg = full.groupby('Title').apply(
    lambda g: pd.Series({
        'ISBN': g['ISBN'].iloc[0],
        'Price': g['Price'].iloc[0],
        'Author': g['Author'].iloc[0],
        'Publisher': g['Publisher'].iloc[0],
        'Publication time': g['Publication time'].iloc[0],
        'Place of Publication': g['Place of Publication'].iloc[0],
        'Pages': g['Pages'].iloc[0],
        'Classification Number': g['Classification Number'].iloc[0],
        '总借入': g['总借入'].sum(),
        '总续借': g['总续借'].sum(),
        '总借入和续借量': g['总借入和续借量'].sum(),
        # 加权平均借阅时间 = 总时长 / 总已归还次数
        '平均借阅时间(天)': round(g['总借阅时长'].sum() / g['已归还次数'].sum(), 2) if g['已归还次数'].sum() > 0 else None
    })
).reset_index()

# ---------- 导出 ----------
title_agg.to_csv('汇总结果_g12.csv', index=False, encoding='utf-8-sig')
print("处理完成！文件已保存为 汇总结果.csv")