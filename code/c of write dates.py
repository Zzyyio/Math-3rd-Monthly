import pandas as pd
import matplotlib.pyplot as plt
import color  # 假设 color.dot_size1, color.dot_color1 已定义

# ---------- 读取 CSV ----------
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果.csv'
df = pd.read_csv(file_path)

# ---------- 提取写作年份 ----------
df["写作日期"] = df["Publication time"].astype(str).str.extract(r'(\d{4})')[0]

# ---------- 去掉缺失数据并排序 ----------
df_write_year = df.dropna(subset=["写作日期", "平均借阅时间(天)", "总借入"])
df_write_year = df_write_year.sort_values("写作日期")









plt.rcParams['font.sans-serif'] = ['Heiti TC']  # macOS 系统自带
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

# ---------- 绘制散点图 ----------
fig, ax = plt.subplots(1, 1, figsize=(8, 5))
ax.scatter(df_write_year['写作日期'],
           df_write_year['平均借阅时间(天)'],
           s=color.dot_size1,
           c=color.dot_color1,
           alpha=0.7)

ax.set_xlabel('Year')
ax.set_ylabel("平均借阅时间（天）")
ax.set_title('写作日期 vs 平均借阅时间')
ax.grid(True)

# ---------- 旋转 x 轴标签 ----------
plt.setp(ax.get_xticklabels(), rotation=45)

plt.tight_layout()  # 避免标签被截断
plt.show()