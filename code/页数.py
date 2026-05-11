import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FixedLocator
import numpy as np
from scipy.optimize import curve_fit

df = pd.read_excel("/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/all.xlsx"
                   ,sheet_name="Sheet1")

df = df[df["Circulation Type"].isin(["外借","续借"])]
# 2️⃣ 提取页数（数字部分）
date_col = "Pages"
df['pages'] = df[date_col].str.extract(r'(\d+)')[0].astype('Int64')


# 4️⃣ 定义页数区间（可根据需要修改）
bins_mid = [75, 125, 175, 225, 275, 325, 375, 425, 475]
bins = [50,100,150,200,250,300,350,400,450,500]
labels = ['50-100', '100-150', '150-200', '200-250', '250-300','300-350', '350-400', '400-450', '450-500']

# 5️⃣ 分页统计
df=df[df['pages'] > 50]
df['pages_range'] = pd.cut(df['pages'], bins=bins, labels=labels, right=False)
counts = df['pages_range'].value_counts().sort_index()

print(counts)
pages_mean=0
indexer=0
for interval in bins_mid[1::]:
    pages_mean += interval*counts.values[indexer]
    indexer += 1
pages_mean /= counts.values.sum()
pages_mean = float(round(pages_mean,2))


def normal_func(x, A, mu, sigma):
    return A * np.exp(-(x-mu)**2 / (2*sigma**2))

# 用 bin_mid 和 counts.values 拟合
popt, _ = curve_fit(normal_func, bins_mid, counts.values, p0=[max(counts.values), pages_mean, 50])


A,mu,sigma=popt
# 拟合曲线
x_smooth = np.linspace(bins_mid[0]-25, bins_mid[-1]+25, 200)
y_smooth = normal_func(x_smooth, *popt)

# ===================== 5. 画图 =====================

plt.rcParams['font.sans-serif'] = ['Heiti TC']  # macOS 系统自带
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

fig, ax = plt.subplots(1, 1, figsize=(8, 5))


ax.bar(bins_mid, counts.values, width=25,color='#4285F4', alpha=0.8)
ax.set_xlabel('页数区间')

ax.xaxis.set_major_locator(MaxNLocator(10))

ax.set_ylabel('借阅/续借次数')
ax.set_title('不同页数的书籍的借阅/续借次数')


ax.plot(x_smooth, y_smooth, color='orange', linestyle='-', label='正态分布拟合')
ax.axvline(x=mu, color='red', linestyle='--',label=f'μ:{mu:.1f}')
width_color="#4285F4"
ax.hlines(y=A*0.5, xmin=mu - sigma, xmax=mu + sigma, color=width_color, linestyle='-', linewidth=2, label=f'σ:{sigma:.1f}')
ax.vlines([mu - sigma, mu + sigma], A*0.5 - 5/2, A*0.5 + 5/2, color=width_color, linewidth=2)


ax.legend()
plt.tight_layout()

plt.savefig('../rendering/页数.png')
plt.show()