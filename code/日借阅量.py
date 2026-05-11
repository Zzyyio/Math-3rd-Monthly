import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FixedLocator

# ===================== 1. 读取数据 =====================
# 请改成你自己的 Excel 文件名
df = pd.read_excel("/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/all.xlsx"
                   ,sheet_name="Sheet1")

# 找到“流通时间”列（你的列名是 Circulation Time）
date_col = "Circulation Time"
print(df.columns.tolist())
# 转成标准日期（去掉时分秒）
df["借阅日期"] = pd.to_datetime(df[date_col]).dt.date

# ===================== 2. 只统计【外借】（可选） =====================
# 如果你要算“所有记录”就注释掉下面这行
df = df[df["Circulation Type"].isin(["外借","续借"])]

# ===================== 3. 统计每天借阅量 =====================
daily = df.groupby(["借阅日期", "Circulation Type"]).size().unstack(fill_value=0).reset_index()
daily["借阅量"]=daily["外借"]+daily["续借"]
daily["借阅日期"] = pd.to_datetime(daily["借阅日期"])
print(daily)

# ===================== 3. 统计每月借阅量 =====================
df["借阅年月"] = df["借阅日期"].apply(lambda x: x.strftime("%Y-%m"))
month = df.groupby(["借阅年月","Circulation Type"]).size().unstack(fill_value=0).reset_index()
# print(month)
month["借阅年月"] = pd.to_datetime(month["借阅年月"])

G10 = df[df["Grade"]=="IB24G10"]
G10_processed = G10.groupby(["借阅年月","Circulation Type"]).size().unstack(fill_value=0).reset_index()
G11 = df[df["Grade"]=="IB23G11"]
G11_processed = G11.groupby(["借阅年月","Circulation Type"]).size().unstack(fill_value=0).reset_index()
G12 = df[df["Grade"]=="IB22G12"]
G12_processed = G12.groupby(["借阅年月","Circulation Type"]).size().unstack(fill_value=0).reset_index()


G10_processed["借阅年月"] = pd.to_datetime(G10_processed["借阅年月"])
G11_processed["借阅年月"] = pd.to_datetime(G11_processed["借阅年月"])
G12_processed["借阅年月"] = pd.to_datetime(G12_processed["借阅年月"])
# ===================== 4. 找出借阅量最高 TOP10 =====================
top10 = daily.nlargest(10, "借阅量").sort_values("借阅量", ascending=True)

# ===================== 5. 画图 =====================

plt.rcParams['font.sans-serif'] = ['Heiti TC']  # macOS 系统自带
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

fig, ((ax1,g10),(ax2,g11),(ax3,g12)) = plt.subplots(3, 2, figsize=(12, 8))

# 上半图：每日借阅量趋势
ax1.bar(daily["借阅日期"], daily["外借"], color="#4285F4", alpha=0.8,label="外借量")
ax1.bar(daily["借阅日期"],daily["续借"],bottom=daily["外借"],color="#428500", alpha=0.8,label="续借量")
ax1.axhline(y=daily["借阅量"].mean(), color="red", linestyle="--", label=f"平均：{daily['借阅量'].mean():.1f}")
ax1.set_title("每日图书借阅量统计", fontsize=14, fontweight="bold")
ax1.set_ylabel("借阅量")
ax1.legend()
ax1.grid(alpha=0.3)
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))


# 下半图：TOP10 日期柱状图
ax2.barh(range(len(top10)), top10["外借"], color="cyan", alpha=0.8,label="外借量")
ax2.barh(range(len(top10)), top10["续借"],left=top10["外借"],color="red",alpha=0.8,label="续借量")
ax2.set_yticks(range(len(top10)))
ax2.set_yticklabels(top10["借阅日期"].dt.strftime("%m-%d"))
ax2.set_xlabel("借阅量")
ax2.set_title("借阅量最高的10个日期", fontweight="bold")
ax2.axvline(x=daily["借阅量"].mean(), color="red", linestyle="--", label=f"平均：{daily['借阅量'].mean():.1f}")
ax2.legend()
# 在柱子上加数字
for i, v in enumerate(top10["借阅量"]):
    ax2.text(v + 0.2, i, str(v), va="center", fontweight="bold")


ax3.bar(month["借阅年月"],month["外借"],color="#4285F4", alpha=0.8,width=10,label="外借量")
ax3.bar(month["借阅年月"],month["续借"],bottom=month["外借"],color="red", alpha=0.8,width=10,label="续借量")

ax3.set_title("每月图书借阅量统计",fontsize=14, fontweight="bold")
ax3.set_ylabel("借阅量")
ax3.grid(alpha=0.3)
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%y-%m"))

bar_width = 10
g10.bar(G10_processed["借阅年月"],G10_processed["外借"],width=bar_width)
g10.bar(G10_processed["借阅年月"],G10_processed["续借"],bottom=G10_processed["外借"],width=bar_width)
g11.bar(G11_processed["借阅年月"],G11_processed["外借"],width=bar_width)
g11.bar(G11_processed["借阅年月"],G11_processed["续借"],bottom=G11_processed["外借"],width=bar_width)
g12.bar(G12_processed["借阅年月"],G12_processed["外借"],width=bar_width)
g12.bar(G12_processed["借阅年月"],G12_processed["续借"],bottom=G12_processed["外借"],width=bar_width)

g10.yaxis.set_major_locator(FixedLocator([0,100,200,300,400,500]))
g11.yaxis.set_major_locator(FixedLocator([0,100,200,300,400,500]))
g12.yaxis.set_major_locator(FixedLocator([0,100,200,300,400,500]))
g11.set_ylim(0, 500)
g12.set_ylim(0, 500)
g10.set_ylim(0, 500)

g10.set_title("G10", fontsize=14, fontweight="bold")
g11.set_title("G11", fontsize=14, fontweight="bold")
g12.set_title("G12", fontsize=14, fontweight="bold")

g10.xaxis.set_major_formatter(mdates.DateFormatter("%y-%m"))
g11.xaxis.set_major_formatter(mdates.DateFormatter("%y-%m"))
g12.xaxis.set_major_formatter(mdates.DateFormatter("%y-%m"))





ax3.legend()
plt.tight_layout()
plt.savefig('../rendering/借阅量.png')
plt.show()