import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import curve_fit


# ===================== 1. 读取数据 =====================
# 请改成你自己的 Excel 文件名
df = pd.read_excel("/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/all.xlsx"
                   ,sheet_name="Sheet1")

#process dataframe
date_col = "Circulation Time"

df["借阅时间段"] = pd.to_datetime(df[date_col]).dt.hour
df = df[df["Circulation Type"].isin(["外借","续借"])]
df["日期"] = pd.to_datetime(df[date_col]).dt.date
df["小时"] = pd.to_datetime(df[date_col]).dt.hour

# 2️⃣ 创建完整的日期-小时组合
all_dates = df["日期"].unique()
all_hours = np.arange(24)
all_combinations = pd.MultiIndex.from_product([all_dates, all_hours], names=["日期", "小时"])

# 3️⃣ 按日期和小时统计借阅量
daily_hourly = df.groupby(["日期", "小时"]).size().reindex(all_combinations, fill_value=0).reset_index(name="借阅量")

# 4️⃣ 按小时计算每日平均
hourly_avg = daily_hourly.groupby("小时")["借阅量"].mean().reset_index(name="平均借阅量")


daily_sum = df.groupby("借阅时间段").size().reset_index(name="借阅量")

daily_separate = df.groupby(["借阅时间段", "Circulation Type"]).size().unstack(fill_value=0).reset_index()
# print(daily_separate)
# print(daily_sum)

#curve fit
borrow_smooth = gaussian_filter1d(daily_sum["借阅量"], sigma=1)
def double_gaussian(x, a1, mu1, sigma1, a2, mu2, sigma2):
    """两个高斯峰叠加"""
    return a1*np.exp(-(x-mu1)**2/(2*sigma1**2)) + a2*np.exp(-(x-mu2)**2/(2*sigma2**2))

#init guessing
peak_indices = daily_sum["借阅量"].argsort()[-2:]
mu1_guess, mu2_guess = sorted(peak_indices)
a1_guess = 100
a2_guess = 90
sigma_guess = 2
initial_guess = [a1_guess, mu1_guess, sigma_guess, a2_guess, mu2_guess, sigma_guess]
#change weights
weights = np.ones_like(borrow_smooth)
weights[mu1_guess-2:mu1_guess+3] = 5   # 第一个峰附近权重5倍
weights[mu2_guess-2:mu2_guess+3] = 5   # 第二个峰附近权重5倍
#set bounds
bounds_lower = [0, 0, 0, 0, 0, 0]
bounds_upper = [np.max(daily_sum["借阅量"]) * 2, 23, 10, np.max(daily_sum["借阅量"]) * 2, 23, 10]
#fit
params, _ = curve_fit(double_gaussian, daily_sum["借阅时间段"], borrow_smooth, p0=initial_guess, bounds=(bounds_lower, bounds_upper), sigma=1 / weights)
a1, mu1, sigma1, a2, mu2, sigma2 =params
print("拟合参数:", params)




#rendering
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

bar_color1='#3673AA'
bar_color2='#4AA6B6'
curve_color='#FF8811'
center_line_color='#F4D035'
width_color='#F4D06F'
fig,ax1 = plt.subplots(1, 1, figsize=(8, 5))



#bar graph
ax1.bar(daily_sum["借阅时间段"], daily_separate["外借"], color=bar_color1, alpha=0.9,label="Borrowings")
ax1.bar(daily_sum["借阅时间段"],daily_separate["续借"],bottom=daily_separate["外借"], color=bar_color2, alpha=0.9,label="Renewals")
#curve graph
x_smooth = np.linspace(0, 23, 200)
y_smooth = double_gaussian(x_smooth, *params)
ax1.plot(x_smooth, y_smooth, color=curve_color, linewidth=2, label='Bimodal Curve')
#set title/label/grid
ax1.set_title("Hourly Borrowings/Renewals Statistics", fontsize=14, fontweight="bold")
ax1.set_ylabel("Total Borrowings/Renewals")
ax1.set_xlabel("Hours")
rax1=ax1.twinx()
rax1.set_ylabel("Average Daily Borrowings/Renewals")
rax1.set_ylim(0, 2.0)
rax1.set_yticks([0,0.5,1.0,1.5,2.0])
ax1.grid(alpha=0.3)
#draw center line(μ)
ax1.axvline(mu1, color=center_line_color, linestyle='-',linewidth=2)
ax1.axvline(mu2, color=center_line_color, linestyle='-', label=f'μ1:{mu1:.1f}\nμ2:{mu2:.1f}',linewidth=2)
#draw width(σ)
y1line = a1*0.5
y2line = a2*0.5
ax1.hlines(y=y1line, xmin=mu1 - sigma1, xmax=mu1 + sigma1, color=width_color, linestyle='-', linewidth=2, label=f'σ1:{sigma1:.1f}\nσ2:{sigma2:.1f}')
ax1.hlines(y=y2line, xmin=mu2 - sigma2, xmax=mu2 + sigma2, color=width_color, linestyle='-', linewidth=2)

cap_height = 5  # 竖线高度
ax1.vlines([mu1 - sigma1, mu1 + sigma1], y1line - cap_height/2, y1line + cap_height/2, color=width_color, linewidth=2)
ax1.vlines([mu2 - sigma2, mu2 + sigma2], y2line - cap_height/2, y2line + cap_height/2, color=width_color, linewidth=2)


ax1.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))

ax1.legend()
plt.tight_layout()
plt.savefig('../rendering/每时间段的借阅量.png')
plt.show()