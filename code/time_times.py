import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../dataset/汇总结果_g12.csv')
df = df.dropna(subset=['平均借阅时间(天)','总借入'])
df = df[df['Classification Number'].str.startswith('IB', na=False)]
fig, (ax)= plt.subplots(1,1,figsize=(5,5))
ax.scatter(df['总借入'],df['平均借阅时间(天)'])
plt.tight_layout()
plt.savefig('../rendering/time_times_g12.png', dpi=300)
plt.show()