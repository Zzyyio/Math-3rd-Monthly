import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------- 数据导入 ----------
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果.csv'
df = pd.read_csv(file_path)

# ---------- 选择需要的列 ----------
columns_needed = ['Classification', '平均借阅时间(天)', '总借入']
df = df[columns_needed]

# ---------- 按分类汇总 ----------
# 计算每个分类的平均借阅时间和总借入次数
grouped = df.groupby('Classification').agg({
    '平均借阅时间(天)': 'mean',
    '总借入': ['sum','mean']
}).reset_index()

# 可选：整理多层列名为单层
grouped.columns = ['Classification', '平均借阅时间(天)', '总借入', '总借入平均量']
# ---------- 设置绘图 ----------
fig, axes = plt.subplots(1, 3, figsize=(14, 6))
fig.suptitle('各书籍分类的借阅情况', fontsize=16)

# # 分类顺序
# categories = ['Arts','Literature', 'Language', 'Social Sciences', 'Science', 'Mathematics', 'General / Misc']



#rendering
plt.rcParams['font.sans-serif'] = ['Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

# ---------- 平均借阅时间柱状图 ----------
axes[0].bar(grouped['Classification'], grouped['平均借阅时间(天)'], color='skyblue')
axes[0].set_title('平均借阅时间 (天)')
axes[0].set_xlabel('书籍分类')
axes[0].set_ylabel('平均借阅时间 (天)')
axes[0].set_xticks(range(len(grouped['Classification'])))
axes[0].set_xticklabels(grouped['Classification'], rotation=30, ha='right')
print(grouped['Classification'],grouped['总借入'])
# ---------- 总借入次数柱状图 ----------
axes[1].pie(grouped['总借入'],labels=grouped['Classification'])
axes[1].set_title('总借入次数')
# axes[1].set_xlabel('书籍分类')
# axes[1].set_ylabel('总借入次数')
# axes[1].set_xticks(range(len(grouped['Classification'])))
# axes[1].set_xticklabels(grouped['Classification'], rotation=30, ha='right')

axes[2].bar(grouped['Classification'],grouped['总借入平均量']*grouped['平均借阅时间(天)'])
axes[2].set_title('总借阅时间')
axes[2].set_xlabel('书籍分类')
axes[2].set_ylabel('总借阅时间')
axes[2].set_xticks(range(len(grouped['Classification'])))
axes[2].set_xticklabels(grouped['Classification'], rotation=30, ha='right')


# ---------- 保存图表 ----------
output_path = '../rendering/time(s)_for_classification.png'
# 确保目录存在
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.tight_layout(rect=[0, 0, 1, 0.95])  # 给 suptitle 留空间
plt.savefig(output_path, dpi=300)

plt.show()
plt.close()
print(f"图表已保存至: {output_path}")