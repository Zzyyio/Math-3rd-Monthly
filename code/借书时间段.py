import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FixedLocator
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import curve_fit

import color

# ===================== 1. 读取数据 =====================
# 请改成你自己的 Excel 文件名
df = pd.read_excel("/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/all.xlsx"
                   ,sheet_name="Sheet1")

#process dataframe
date_col = "Circulation Time"

df["借阅时间段"] = pd.to_datetime(df[date_col]).dt.hour
df = df[df["Circulation Type"].isin(["外借","续借"])]


daily_sum = df.groupby("借阅时间段").size().reset_index(name="借阅量")

daily_separate = df.groupby(["借阅时间段", "Circulation Type"]).size().unstack(fill_value=0).reset_index()

IB24G10=df[df["Grade"]=="IB24G10"]
IB23G11=df[df["Grade"]=="IB23G11"]
IB22G12=df[df["Grade"]=="IB22G12"]
IB24G10_processed = IB24G10.groupby(["借阅时间段","Circulation Type"]).size().unstack(fill_value=0).reset_index()
IB23G11_processed = IB23G11.groupby(["借阅时间段","Circulation Type"]).size().unstack(fill_value=0).reset_index()
IB22G12_processed = IB22G12.groupby(["借阅时间段","Circulation Type"]).size().unstack(fill_value=0).reset_index()

def fill_missing_hours(df_processed):
    hours = pd.DataFrame({"借阅时间段": np.arange(0,24)})
    df_filled = pd.merge(hours, df_processed, on="借阅时间段", how="left")
    # 没有的类型填 0
    for col in ["外借", "续借"]:
        if col in df_filled.columns:
            df_filled[col] = df_filled[col].fillna(0)
        else:
            df_filled[col] = 0
    return df_filled

IB24G10_processed = fill_missing_hours(IB24G10_processed)
IB23G11_processed = fill_missing_hours(IB23G11_processed)
IB22G12_processed = fill_missing_hours(IB22G12_processed)

print(IB24G10_processed, IB23G11_processed, IB22G12_processed)
print(daily_separate)
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

output_location="/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/output_dataset/op.xlsx"
daily_sum.to_excel(output_location, sheet_name="Sheet1")

#rendering
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示



curve_color=color.line_color1
center_line_color=color.line_color1
width_color=color.line_color1
fig,((ax1 ,g10),(g11,g12))= plt.subplots(2, 2, figsize=(15, 8))

def set_twin_label(ax):
    axx = ax.twinx()
    axx.set_ylabel("Average Daily Borrowings/Renewals")
    axx.set_ylim(0, 2.0)
    axx.set_yticks([0, 0.5, 1.0, 1.5, 2.0])

#bar graph
ax1.bar(daily_sum["借阅时间段"], daily_separate["外借"], color=color.bar_color1, alpha=0.9,label="Borrowings")
ax1.bar(daily_sum["借阅时间段"],daily_separate["续借"],bottom=daily_separate["外借"], color=color.bar_color2, alpha=0.9,label="Renewals")
#curve graph
x_smooth = np.linspace(0, 23, 200)
y_smooth = double_gaussian(x_smooth, *params)
ax1.plot(x_smooth, y_smooth, color=curve_color, linewidth=1, label='Bimodal Curve')
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
ax1.axvline(mu1, color=center_line_color, linestyle='--',linewidth=1)
ax1.axvline(mu2, color=center_line_color, linestyle='--', label=f'μ1:{mu1:.1f}\nμ2:{mu2:.1f}',linewidth=1)
#draw width(σ)
y1line = a1*0.5
y2line = a2*0.5
ax1.hlines(y=y1line, xmin=mu1 - sigma1, xmax=mu1 + sigma1, color=width_color, linestyle='--', linewidth=1, label=f'σ1:{sigma1:.1f}\nσ2:{sigma2:.1f}')
ax1.hlines(y=y2line, xmin=mu2 - sigma2, xmax=mu2 + sigma2, color=width_color, linestyle='--', linewidth=1)

cap_height = 5  # 竖线高度
ax1.vlines([mu1 - sigma1, mu1 + sigma1], y1line - cap_height/2, y1line + cap_height/2, color=width_color, linewidth=2)
ax1.vlines([mu2 - sigma2, mu2 + sigma2], y2line - cap_height/2, y2line + cap_height/2, color=width_color, linewidth=2)


ax1.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))

g10.bar(IB24G10_processed["借阅时间段"],IB24G10_processed["外借"],color=color.bar_color1,label="Borrowings")
g10.bar(IB24G10_processed["借阅时间段"],IB24G10_processed["续借"],color=color.bar_color2,bottom=IB24G10_processed["外借"],label="Renewals")
g11.bar(IB23G11_processed["借阅时间段"],IB23G11_processed["外借"],color=color.bar_color1,label="Borrowings")
g11.bar(IB23G11_processed["借阅时间段"],IB23G11_processed["续借"],color=color.bar_color2,bottom=IB23G11_processed["外借"],label="Renewals")
g12.bar(IB22G12_processed["借阅时间段"],IB22G12_processed["外借"],color=color.bar_color1,label="Borrowings")
g12.bar(IB22G12_processed["借阅时间段"],IB22G12_processed["续借"],color=color.bar_color2,bottom=IB22G12_processed["外借"],label="Renewals")

g10.xaxis.set_major_locator(FixedLocator([0,3,6,9,12,15,18,21,24]))
g11.xaxis.set_major_locator(FixedLocator([0,3,6,9,12,15,18,21,24]))
g12.xaxis.set_major_locator(FixedLocator([0,3,6,9,12,15,18,21,24]))


set_twin_label(g10)
set_twin_label(g11)
set_twin_label(g12)

g10.set_title("G10", fontsize=14, fontweight="bold")
g11.set_title("G11", fontsize=14, fontweight="bold")
g12.set_title("G12", fontsize=14, fontweight="bold")

g11.set_ylim(0, 350)
g12.set_ylim(0, 350)
g10.set_ylim(0, 350)

g10.set_xlabel("Hours")
g11.set_xlabel("Hours")
g12.set_xlabel("Hours")
ax1.legend()
g10.legend()
g11.legend()
g12.legend()
plt.tight_layout()
plt.savefig('../rendering/每时间段的借阅量.png')
plt.show()