import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FixedLocator

#import data
df = pd.read_excel("/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/all.xlsx"
                   ,sheet_name="Sheet1")
df = df[df["Circulation Type"].isin(["外借","续借"])]

date_col = "Publication time"

df["写作日期"] = df[date_col].astype(str).str.extract(r'(\d{4})')[0] # 读取年份
df["写作日期"] = pd.to_numeric(df["写作日期"], errors='coerce')
df = df.dropna(subset=["写作日期"])
df["写作日期"] = df["写作日期"].astype(int)

year = df.groupby("写作日期").size().reset_index(name="数量")


year_for_cal = df.groupby("写作日期").size().reset_index(name="数量")
year_mean = (year_for_cal['写作日期'] * year_for_cal['数量']).sum() / year_for_cal['数量'].sum()

#rendering
plt.rcParams['font.sans-serif'] = ['Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

fig, borrow_sum = plt.subplots(1, 1, figsize=(8, 5))


borrow_sum.bar(year["写作日期"], year["数量"], color="#4285F4", alpha=0.8, width=0.5)
borrow_sum.axvline(x=year_mean, color="red", linestyle="--", label=f'center:{year_mean:.0f}')
borrow_sum.legend()
borrow_sum.set_title("借阅/续借量关于写作日期的分布", fontsize=14, fontweight="bold")
borrow_sum.set_ylabel("该年写作的书的总借阅/续借量（本）")
borrow_sum.grid(alpha=0.3)


borrow_sum.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))




plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../rendering/写作日期_int.png")
plt.show()


