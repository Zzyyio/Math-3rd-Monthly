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

# 4️⃣ 定义页数区间（可根据需要修改）
bins_mid = [12.5, 37.5, 62.5, 87.5, 112.5, 137.5, 162.5, 187.5, 212.5, 237.5, 262.5, 287.5, 312.5, 337.5, 362.5, 387.5, 412.5, 437.5, 462.5, 487.5]
bins = [0,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500]
labels = ["0-25","25-50","50-75","75-100","100-125","125-150","150-175","175-200","200-225","225-250","250-275","275-300","300-325","325-350","350-375","375-400","400-425","425-450","450-475","475-500"]

# 5️⃣ 分页统计
# df=df[df['pages'] > 50]
df['prices_range'] = pd.cut(df['price'], bins=bins, labels=labels, right=False)
counts = df['prices_range'].value_counts().sort_index()




G10_processed,G11_processed,G12_processed=cal_for_three_class.price_process(df,"prices_range",bins,labels)
counts_separate = df.groupby(["prices_range", "Circulation Type"]).size().unstack(fill_value=0).reset_index()


def normal_func(x, A, mu, sigma):
    return A * np.exp(-(x-mu)**2 / (2*sigma**2))

# ===================== 5. 画图 =====================

plt.rcParams['font.sans-serif'] = ['Heiti TC']  # macOS 系统自带
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

fig, ((ax,g10),(g11,g12)) = plt.subplots(2, 2, figsize=(14, 8))


ax.bar(bins_mid, counts_separate["外借"], width=10,color=color.bar_color1, alpha=color.alpha,label="Borrowings")
ax.bar(bins_mid, counts_separate["续借"], bottom=counts_separate["外借"],color=color.bar_color2,width=10, alpha=color.alpha,label="Renewals")
ax.set_xlabel('Page Intervals')

ax.xaxis.set_major_locator(FixedLocator(bins))

ax.set_ylabel('Borrowings/Renewals')
ax.set_title('Borrowings/Renewals of different pages')


vh_color=color.line_color1
line_color=color.line_color1

width_color=color.line_color1

cal_for_three_class.price_show(g10, g11, g12, G10_processed, G11_processed, G12_processed, bins_mid, "外借", 10,
                               alpha=color.alpha,bins=bins)
ax.legend()
plt.tight_layout()

plt.savefig('../rendering/价格.png')
plt.show()