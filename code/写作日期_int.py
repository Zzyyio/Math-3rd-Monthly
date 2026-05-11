import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.optimize import curve_fit
from scipy.stats import lognorm, gamma

df = pd.read_excel("/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/all.xlsx"
                   ,sheet_name="Sheet1")
df = df[df["Circulation Type"].isin(["外借","续借"])]

date_col = "Publication time"

df["写作日期"] = df[date_col].astype(str).str.extract(r'(\d{4})')[0]
df["写作日期"] = pd.to_numeric(df["写作日期"], errors='coerce')
df = df.dropna(subset=["写作日期"])
df["写作日期"] = df["写作日期"].astype(int)

# 2️⃣ 按年份统计借阅次数
year = df.groupby("写作日期").size().reset_index(name="数量")

# 3️⃣ 计算加权平均
year_mean = (year['写作日期'] * year['数量']).sum() / year['数量'].sum()

#创建绘图索引（删除空白年份）
x_pos = np.arange(len(year))



#curvefit

# # 1️⃣ 准备数据：按数量展开每年的年份
# # 让每个年份重复对应数量次，用于拟合分布
# data_for_fit = np.repeat(year['写作日期'].values, year['数量'].values)
#
# # 2️⃣ 拟合对数正态分布
# shape, loc, scale = lognorm.fit(data_for_fit, floc=0,fscale=0)  # 固定 loc=0，更稳定
# print(shape, loc, scale)
# # 3️⃣ 生成 x 范围
# x_fit = np.linspace(year['写作日期'].min(), year['写作日期'].max(), 500)
#
# # 4️⃣ 计算概率密度函数
# pdf = lognorm.pdf(x_fit, s=shape, loc=loc, scale=scale)

#自动选择刻度
max_ticks = 10
if len(x_pos) <= max_ticks:
    tick_positions = x_pos
else:
    tick_indices = np.linspace(0, len(x_pos) - 1, max_ticks, dtype=int)
    tick_positions = x_pos[tick_indices]
# 生成对应的刻度标签
tick_labels = year['写作日期'].iloc[tick_positions].tolist()
# 假设右偏，使用单峰指数衰减或自定义函数
def gamma_like(x, a, b, c,d):
    return a * ((-x+d)**(b-1)) * np.exp((x-d)/c)

x_data = year['写作日期'].values
x_data_scaled = x_data - x_data.min() + 1
y_data = year['数量'].values

params, cov = curve_fit(gamma_like, x_data_scaled, y_data, p0=[max(y_data), 1.5, 10,2000],maxfev=800)
print(params)
# 绘制拟合曲线
x_fit = np.linspace(x_data.min(), x_data.max(), 500)
y_fit = gamma_like(x_fit, *params)
x_fit = x_fit + x_data.min() - 1

# 缩放到柱状图高度
# pdf_scaled = pdf * year["数量"].sum() * (x_pos[1]-x_pos[0])







#rendering
plt.rcParams['font.sans-serif'] = ['Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
#create graph
fig, borrow_sum = plt.subplots(1, 1, figsize=(8, 5))

#create bar
borrow_sum.bar(x_pos, year["数量"], color="#4285F4", alpha=0.8, width=0.5)
# 映射加权平均到索引位置
year_mean = np.interp(year_mean, year['写作日期'], x_pos)
borrow_sum.axvline(x=year_mean, color="red", linestyle="--", label=f'center:{year_mean:.0f}')
borrow_sum.set_title("借阅/续借量关于写作日期的分布", fontsize=14, fontweight="bold")
borrow_sum.set_ylabel("该年写作的书的总借阅/续借量（本）")
borrow_sum.grid(alpha=0.3)


#自动选择刻度
max_ticks = 10
if len(x_pos) <= max_ticks:
    tick_positions = x_pos
else:
    tick_indices = np.linspace(0, len(x_pos) - 1, max_ticks, dtype=int)
    tick_positions = x_pos[tick_indices]
# 生成对应的刻度标签
tick_labels = year['写作日期'].iloc[tick_positions].tolist()
#绘制xlabel
borrow_sum.set_xticks(tick_positions)
borrow_sum.set_xticklabels(tick_labels, rotation=45)



borrow_sum.plot(np.interp(x_fit, x_data, x_pos), y_fit, color='orange', label='Gamma-like fit')


borrow_sum.legend()
plt.tight_layout()
plt.savefig("../rendering/写作日期_int.png")
plt.show()


