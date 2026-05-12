import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FixedLocator
import numpy as np
from scipy.optimize import curve_fit
from scipy.special import gamma


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


# ------------------ 定义 Gamma 拟合函数 ------------------
# Gamma PDF: f(x; a, scale) = x**(a-1) * exp(-x/scale) / (gamma(a) * scale**a)
# 我们加一个整体放缩参数 A
def gamma_func(x, A, a, scale):
    return A * (x**(a-1) * np.exp(-x/scale))

# 初始猜测值: A=max(counts), a=2, scale=mean/2
p0 = [200, 1.2, 20]

# 拟合
popt, _ = curve_fit(gamma_func, small_bins_mid, small_counts.values, p0=p0, maxfev=10000 )
A_fit, a_fit, theta_fit = popt


# 计算衍生参数
mode = (a_fit - 1) * theta_fit if a_fit > 1 else 0
mean = a_fit * theta_fit
var = a_fit * theta_fit**2
sigma = np.sqrt(var)
fmax = gamma_func(mode, A_fit, a_fit, theta_fit)


print(popt)
# 拟合曲线
x_smooth = np.linspace(small_bins_mid[0]-25, small_bins_mid[-1]+25, 200)
y_smooth = gamma_func(x_smooth, *popt)


vh_color = color.line_color1
line_color = color.line_color1
width_color = color.line_color1


# ===================== 5. 画图 =====================

plt.rcParams['font.sans-serif'] = ['Heiti TC']  # macOS 系统自带
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

fig, zoomin = plt.subplots(1, 1, figsize=(14, 8))

vh_color=color.line_color1
line_color=color.line_color1

width_color=color.line_color1
# 拟合曲线
zoomin.plot(x_smooth, y_smooth, color=line_color, linestyle='-', label='gamma curve')

# 用 Gamma 分布的峰值位置 (mode = (a-1)*scale) 画虚线
mode = (a_fit - 1) * theta_fit if a_fit > 1 else 0
zoomin.axvline(x=mode, color=vh_color, linestyle='dashdot', linewidth=1, label=f'mode:{mode:.1f}')

print(a_fit)
# 可以用 y = A*0.5 做宽度参考

# width_location=A_fit*0.5
# zoomin.hlines(y=width_location, xmin=mode - theta_fit, xmax=mode + theta_fit,
#                color=width_color, linestyle='--', linewidth=1, label=f'scale:{a_fit:.1f}')
# zoomin.vlines([mode - theta_fit, mode + theta_fit], width_location - 5/2, width_location + 5/2,
#                color=width_color, linewidth=2)





zoomin.bar(small_bins_mid,small_counts_separate["外借"],width=5,color=color.bar_color1,label="外借")
zoomin.bar(small_bins_mid,small_counts_separate["续借"],bottom=small_counts_separate["外借"],width=5,color=color.bar_color2,label="续借")

zoomin.xaxis.set_major_locator(FixedLocator(small_bins))

zoomin.legend()

zoomin.set_title("Borrowings/Renewals of different prices(Zoomed Version)")
zoomin.set_xlabel("Price intervals")
zoomin.set_ylabel("Borrowings/Renewals")
plt.tight_layout()

plt.savefig('../rendering/页数.png')
plt.show()