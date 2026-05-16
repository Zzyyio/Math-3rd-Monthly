import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd



# 假设 df_corr 是相关性矩阵
df_corr = pd.read_csv('../output_dataset/analysis_outputs/association_mutual_info.csv', header=0, index_col=0).fillna(0)



plt.rcParams['font.sans-serif'] = ['Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

plt.figure(figsize=(8, 7))

sns.heatmap(df_corr, annot=True, cmap='coolwarm', center=0)
# plt.xticks(rotation=20)
plt.title("Mutual Correlation Heatmap")
plt.tight_layout()
plt.savefig('../rendering/heatmap_mutual.png', dpi=300)
plt.show()