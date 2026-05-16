import pandas as pd
import matplotlib.pyplot as plt
import color
# ---------- 设置中文显示 ----------
plt.rcParams['font.sans-serif'] = ['Heiti TC']  # 中文字体
plt.rcParams['axes.unicode_minus'] = False      # 负号正常显示

# ---------- 读取数据 ----------
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果_with_rating_classification.csv'
df = pd.read_csv(file_path)

# ---------- 检查关键列是否存在 ----------

df=df[df['rating']!='暂无评分']
required_columns = ['rating', '平均借阅时间(天)', '总借入和续借量']
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# 计算借阅频率
total_borrows = df['总借入和续借量'].sum()
df['借阅频率'] = df['总借入和续借量'] / total_borrows




# 按 rating 升序排序，并只保留所需列
df_sorted = df[required_columns].sort_values(by='rating', ascending=True)
df_sorted['总借阅时长']=df_sorted['平均借阅时间(天)']*df_sorted['总借入和续借量']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"数据集中缺少列: {col}")

# ---------- 绘制散点图 ----------
fig, axes = plt.subplots(1, 3, figsize=(14, 6))

fig1 = plt.figure(figsize=(10,8))
ax = fig1.add_subplot(111, projection='3d')

# rating vs 平均借阅时间(天)
axes[0].scatter(df_sorted['rating'], df_sorted['平均借阅时间(天)'], color='skyblue',s=color.dot_size1)
axes[0].set_xlabel('Rating')
axes[0].set_ylabel('Average Borrowing Duration')
axes[0].set_title('Rating vs. Average Borrowing Duration')

# rating vs 总借入和续借量
axes[1].scatter(df_sorted['rating'], df_sorted['总借入和续借量'], color='salmon',s=color.dot_size1,alpha=0.5)
axes[1].set_xlabel('Rating')
axes[1].set_ylabel('Total Borrowing/Renewal Counts')
axes[1].set_title('Rating vs. Total Borrowing Counts')


axes[2].scatter(df_sorted['rating'], df_sorted['总借阅时长'], color='salmon',s=color.dot_size1)
axes[2].set_xlabel('Rating')
axes[2].set_ylabel('Average Total Borrowing Duration')
axes[2].set_title('Rating vs. Average Total Borrowing Duration')
# ---------- 图表布局优化 ----------
plt.tight_layout()

output_path = '../rendering/time(s)_vs_rating.png'
fig.savefig(output_path, dpi=300)

scatter = ax.scatter(df_sorted['rating'],  df_sorted['平均借阅时间(天)'],df_sorted['总借入和续借量'],
                     c=df_sorted['平均借阅时间(天)'], cmap='viridis',   # 用总借入和续借量次数上色
                     s=color.dot_size1,
                     alpha=0.8)

cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=10)
cbar.set_label('总借入和续借量次数')

ax.set_xlim(df_sorted['rating'].min() - 0.1, df_sorted['rating'].max() + 0.1)

# ---------- 图表布局优化 ----------
plt.tight_layout()

# ---------- 保存图表 ----------
output_path = '../rendering/time(s)_vs_rating_3d.png'
fig1.savefig(output_path, dpi=300)
plt.show()