import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/all.xlsx"
                   ,sheet_name="Sheet1")

df = df[df["Circulation Type"].isin(["外借","续借"])]
# 2️⃣ 提取页数（数字部分）
date_col = "Pages"
df['pages'] = df[date_col].str.extract(r'(\d+)')[0].astype('Int64')


# 4️⃣ 定义页数区间（可根据需要修改）
bins = [50,100, 150, 200, 250,300,350,400,450,500]

labels = ['50-100', '100-150', '150-200', '200-250', '250-300','300-350', '350-400', '400-450', '450-500']

# 5️⃣ 分页统计
df=df[df['pages'] > 50]
df['pages_range'] = pd.cut(df['pages'], bins=bins, labels=labels, right=False)
counts = df['pages_range'].value_counts().sort_index()

print(counts)
pages_mean=0
indexer=0
for interval in bins[1::]:
    pages_mean += interval*counts.values[indexer]
    indexer += 1
pages_mean /= counts.values.sum()
pages_mean=str(round(pages_mean,0))
print(counts)
print(df['pages'].mean())


# ===================== 5. 画图 =====================

plt.rcParams['font.sans-serif'] = ['Heiti TC']  # macOS 系统自带
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示


plt.figure(figsize=(8,5))
plt.bar(counts.index, counts.values, color='#4285F4', alpha=0.8)
plt.xlabel('页数区间')
plt.ylabel('借阅/续借次数')
plt.title('不同页数的书籍的借阅/续借次数')
plt.axvline(x=pages_mean, color='r', linestyle='--')
plt.tight_layout()

plt.savefig('../rendering/页数.png')
plt.show()