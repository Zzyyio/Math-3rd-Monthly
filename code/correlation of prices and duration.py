import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import stats

import color
# ---------- 读取 CSV ----------
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果.csv'
df = pd.read_csv(file_path)

# ---------- 处理 prices 列 ----------
# def extract_page_number(prices_str):
#     if pd.isna(prices_str):
#         return None
#     # 只取开头的数字
#     for char in prices_str:
#         if not char.isdigit():
#             break
#     num = ''.join([c for c in prices_str if c.isdigit()])
#     return int(num) if num else None
#
# df['Price'] = df['prices'].apply(extract_page_number)



# ---------- 去掉 prices 为空的数据 ----------
df_clean = df.dropna(subset=['Price', '平均借阅时间(天)','总借入'])
df_clean['lend_time_sum']=df_clean["总借入"]*df_clean['平均借阅时间(天)']
print(df_clean['Price'], df_clean['lend_time_sum'],df_clean['平均借阅时间(天)'])



plt.rcParams['font.sans-serif'] = ['Heiti TC']  # macOS 系统自带
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示


# ---------- 绘制散点图 ----------

fig, (lend_duration_sum,lend_times) = plt.subplots(2,1,figsize=(10,10))

print(stats.pearsonr(df_clean['Price'], df_clean['lend_time_sum']))
print(stats.spearmanr(df_clean['Price'], df_clean['lend_time_sum']))
lend_duration_sum.scatter(df_clean['Price'], df_clean['lend_time_sum'],s=color.dot_size1,c=color.dot_color1)
lend_duration_sum.set_xlabel('prices')
lend_duration_sum.set_ylabel('average borrowing duration')
lend_duration_sum.set_title('Scatter plot of book price vs. average borrowing duration')
lend_duration_sum.grid(True)


print(stats.pearsonr(df_clean['Price'], df_clean['总借入']))
print(stats.spearmanr(df_clean['Price'], df_clean['总借入']))
lend_times.scatter(df_clean['Price'],df_clean['总借入'],s=color.dot_size1,c=color.dot_color1)
lend_times.set_xlabel('prices')
lend_times.set_ylabel('Total borrow count per book')
lend_times.grid(True)
lend_times.set_title('Scatter plot of book price vs. total borrow count')



plt.savefig('../rendering/prices_vs_times&prices_vs_duration.png')
plt.show()