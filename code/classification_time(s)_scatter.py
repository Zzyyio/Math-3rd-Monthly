import pandas as pd
import matplotlib.pyplot as plt
import color
# ---------- 保证中文显示 ----------
plt.rcParams['font.sans-serif'] = ['Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

# ---------- 读取数据 ----------
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果_g11.csv'
df = pd.read_csv(file_path)

# ---------- 准备颜色映射 ----------
classifications = ['Literature','Language','Social Sciences','Science','Mathematics','General / Misc']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']  # 每个分类一个颜色
color_map = dict(zip(classifications, colors))

# ---------- 绘制散点图 ----------
# plt.figure(figsize=(10, 6))
fig=plt.figure(figsize=(6,6))
ax=fig.add_subplot(projection='3d')
i=1

subsets = df[df['Classification']=='General / Misc']
print(len(subsets))
for cls in classifications:
    subset = df[df['Classification'] == cls]
    ax.scatter(
        subset['平均借阅时间(天)'],
        subset['总借入'],
        i,
        label=cls,
        color=color_map[cls],
        s=color.dot_size1,
        alpha=0.4
    )
    i=i+1

# ---------- 图表美化 ----------
plt.xlabel('Average Borrowing Duration', fontsize=12)
plt.ylabel('Checkout Times', fontsize=12)
plt.title('Relationship between Average Borrowing Duration \nand Checkout Times by Book Category-G11', fontsize=14)
plt.legend(title='Classification')
plt.grid(True, linestyle='--', alpha=0.5)

# ---------- 保存图表 ----------
plt.tight_layout()
plt.savefig('../rendering/class_vs_time_scatter_g11.png', dpi=300)
plt.show()