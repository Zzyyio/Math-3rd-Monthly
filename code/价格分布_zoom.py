import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FixedLocator
import numpy as np
from scipy.optimize import curve_fit
import cal_for_three_class
import color


df = pd.read_excel("/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/all.xlsx"
                   ,sheet_name="Sheet1")

df = df[df["Circulation Type"].isin(["外借","续借"])]
# 2️⃣ 提取页数（数字部分）
date_col = "Price"
df['price'] = df[date_col]
small_bins = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150]
small_bins_mid = [5,15,25,35,45,55,65,75,85,95,105,115,125,135,145]


df['small_price_range'] = pd.cut(df['price'], bins=small_bins, right=False)
small_counts = df['small_price_range'].value_counts().sort_index()
small_counts_separate = df.groupby(["small_price_range", "Circulation Type"]).size().unstack(fill_value=0).reset_index()




small_price_mean=0
indexer=0
for interval in small_bins_mid[1::]:
    small_price_mean += interval * small_counts.values[indexer]
    indexer += 1
small_price_mean /= small_counts.values.sum()
small_price_mean = float(round(small_price_mean, 2))


def normal_func(x, A, mu, sigma):
    return A * np.exp(-(x-mu)**2 / (2*sigma**2))

# 用 bin_mid 和 counts.values 拟合
popt, _ = curve_fit(normal_func, small_bins_mid, small_counts.values, p0=[max(small_counts.values), small_price_mean, 50])


A,mu,sigma=popt
# 拟合曲线
x_smooth = np.linspace(small_bins_mid[0]-25, small_bins_mid[-1]+25, 200)
y_smooth = normal_func(x_smooth, *popt)

# ===================== 5. 画图 =====================

plt.rcParams['font.sans-serif'] = ['Heiti TC']  # macOS 系统自带
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

fig, zoomin = plt.subplots(1, 1, figsize=(14, 8))

vh_color=color.line_color1
line_color=color.line_color1

width_color=color.line_color1

zoomin.plot(x_smooth, y_smooth, color=line_color, linestyle='-', label='norm curve')
zoomin.axvline(x=mu, color=vh_color, linestyle='dashdot',linewidth=1,label=f'μ:{mu:.1f}(Pages)')


zoomin.hlines(y=A*0.5, xmin=mu - sigma, xmax=mu + sigma, color=width_color, linestyle='--', linewidth=1, label=f'σ:{sigma:.1f}')
zoomin.vlines([mu - sigma, mu + sigma], A*0.5 - 5/2, A*0.5 + 5/2, color=width_color, linewidth=2)

zoomin.bar(small_bins_mid,small_counts_separate["外借"],width=5,color=color.bar_color1)
zoomin.bar(small_bins_mid,small_counts_separate["续借"],bottom=small_counts_separate["外借"],width=5,color=color.bar_color2)

zoomin.xaxis.set_major_locator(FixedLocator(small_bins))

zoomin.legend()

plt.tight_layout()

plt.savefig('../rendering/页数.png')
plt.show()