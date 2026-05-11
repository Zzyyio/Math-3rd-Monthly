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
date_col = "Pages"
df['pages'] = df[date_col].str.extract(r'(\d+)')[0].astype('Int64')


# 4️⃣ 定义页数区间（可根据需要修改）
bins_mid = [75, 125, 175, 225, 275, 325, 375, 425, 475,525,575,625,675,725,775,825,875,925,975]
bins = [50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000]
labels = ['50-100', '100-150', '150-200', '200-250', '250-300','300-350', '350-400', '400-450', '450-500',"500-550","550-600","600-650","650-700","700-750","750-800","800-850","850-900","900-950","950-1000"]

# 5️⃣ 分页统计
df=df[df['pages'] > 50]
df['pages_range'] = pd.cut(df['pages'], bins=bins, labels=labels, right=False)
counts = df['pages_range'].value_counts().sort_index()


G10_processed,G11_processed,G12_processed=cal_for_three_class.page_process(df,"pages_range",bins,labels)
print(G10_processed)
counts_separate = df.groupby(["pages_range", "Circulation Type"]).size().unstack(fill_value=0).reset_index()
# print(counts_separate)
# print(counts)
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

fig, ((ax,g10),(g11,g12)) = plt.subplots(2, 2, figsize=(14, 8))


ax.bar(bins_mid, counts_separate["外借"], width=35,color=color.bar_color1, alpha=0.8,label="Borrowings")
ax.bar(bins_mid, counts_separate["续借"], bottom=counts_separate["外借"],color=color.bar_color2,width=35, alpha=1,label="Renewals")
ax.set_xlabel('Page Intervals')

ax.xaxis.set_major_locator(MaxNLocator(21))

ax.set_ylabel('Borrowings/Renewals')
ax.set_title('Borrowings/Renewals of different pages')
vh_color=color.line_color1
line_color=color.line_color1

ax.plot(x_smooth, y_smooth, color=line_color, linestyle='-', label='norm curve')
ax.axvline(x=mu, color=vh_color, linestyle='dashdot',linewidth=1,label=f'μ:{mu:.1f}(Pages)')
width_color=vh_color
ax.hlines(y=A*0.5, xmin=mu - sigma, xmax=mu + sigma, color=width_color, linestyle='--', linewidth=1, label=f'σ:{sigma:.1f}')
ax.vlines([mu - sigma, mu + sigma], A*0.5 - 5/2, A*0.5 + 5/2, color=width_color, linewidth=2)

cal_for_three_class.page_show(g10,g11,g12,G10_processed,G11_processed,G12_processed,bins_mid,"外借",35)
ax.legend()
plt.tight_layout()

plt.savefig('../rendering/页数.png')
plt.show()