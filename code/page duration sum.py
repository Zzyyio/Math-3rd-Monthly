import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 新版可不显式导入
import color  # 自定义颜色模块

# ---------- 读取 CSV ----------
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果.csv'
df = pd.read_csv(file_path)

# ---------- 提取页数 ----------
df['pages_num'] = df["Pages"].str.extract(r'(\d+)')[0].astype('Int64')
df = df[df['pages_num'] > 50]

# ---------- 清洗数据 ----------
df_clean = df.dropna(subset=['pages_num', '平均借阅时间(天)','总借入'])
df_clean['lend_time_sum'] = df_clean["总借入"] * df_clean['平均借阅时间(天)']

# ---------- 3D 散点图 ----------
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

# x = 页数, y = 平均借阅时间, z = 总借入次数
x = df_clean['pages_num']
y = df_clean['平均借阅时间(天)']
z = df_clean['总借入']




plt.rcParams['font.sans-serif'] = ['Heiti TC']  # macOS 系统自带
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示



scatter = ax.scatter(x, y, z,
                     c=z, cmap='viridis',   # 用总借入次数上色
                     s=color.dot_size1,
                     alpha=0.8)

ax.set_xlabel('Pages')
ax.set_ylabel('平均借阅时间(天)')
ax.set_zlabel('总借入次数')
ax.set_title('书籍页数 vs 平均借阅时间 vs 总借入次数三维散点图')

# 添加颜色条
cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=10)
cbar.set_label('总借入次数')

# 显示网格
ax.grid(True)

plt.tight_layout()
plt.savefig('../rendering/pages_vs_times_vs_lend3D.png')
plt.show()