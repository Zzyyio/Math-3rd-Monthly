import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
daily = df.groupby("借阅日期").size().reset_index(name="借阅量")
daily["借阅日期"] = pd.to_datetime(daily["借阅日期"])
print(daily)

# ===================== 3. 统计每月借阅量 =====================
df["借阅年月"] = df["借阅日期"].apply(lambda x: x.strftime("%Y-%m"))
month = df.groupby("借阅年月").size().reset_index(name="借阅量")
# print(month)
month["借阅年月"] = pd.to_datetime(month["借阅年月"])

# ===================== 4. 找出借阅量最高 TOP10 =====================
top10 = daily.nlargest(10, "借阅量").sort_values("借阅量", ascending=True)

# ===================== 5. 画图 =====================

plt.rcParams['font.sans-serif'] = ['Heiti TC']  # macOS 系统自带
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

fig, (ax1,ax2,ax3) = plt.subplots(3, 1, figsize=(8, 10))

# 上半图：每日借阅量趋势
ax1.bar(daily["借阅日期"], daily["借阅量"], color="#4285F4", alpha=0.8)
ax1.axhline(y=daily["借阅量"].mean(), color="red", linestyle="--", label=f"平均：{daily['借阅量'].mean():.1f}")
ax1.set_title("每日图书借阅量统计", fontsize=14, fontweight="bold")
ax1.set_ylabel("借阅量")
ax1.legend()
ax1.grid(alpha=0.3)
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))


ax3.xaxis.set_major_formatter(mdates.DateFormatter("%y-%m"))
# 下半图：TOP10 日期柱状图
ax2.barh(range(len(top10)), top10["借阅量"], color="cyan", alpha=0.8)
ax2.set_yticks(range(len(top10)))
ax2.set_yticklabels(top10["借阅日期"].dt.strftime("%m-%d"))
ax2.set_xlabel("借阅量")
ax2.set_title("借阅量最高的10个日期", fontweight="bold")
ax2.axvline(x=daily["借阅量"].mean(), color="red", linestyle="--", label=f"平均：{daily['借阅量'].mean():.1f}")
ax2.legend()
# 在柱子上加数字
for i, v in enumerate(top10["借阅量"]):
    ax2.text(v + 0.2, i, str(v), va="center", fontweight="bold")


ax3.bar(month["借阅年月"],month["借阅量"],color="#4285F4", alpha=0.8,width=10)
ax3.set_title("每月图书借阅量统计",fontsize=14, fontweight="bold")
ax3.set_ylabel("借阅量")
ax3.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('../rendering/借阅量.png')
plt.show()