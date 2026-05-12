import pandas as pd
import matplotlib.pyplot as plt
import color
#naaaa！

# ---------- 读取 CSV ----------
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果.csv'
df = pd.read_csv(file_path)



# ---------- 去掉缺失数据并排序 ----------
df_dur_feq = df.dropna(subset=[ "平均借阅时间(天)", "总借入"])
df_dur_feq = df_dur_feq.sort_values("平均借阅时间(天)")









plt.rcParams['font.sans-serif'] = ['Heiti TC']  # macOS 系统自带
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

# ---------- 绘制散点图 ----------
fig, ax = plt.subplots(1, 1, figsize=(8, 5))
ax.scatter(df_dur_feq['平均借阅时间(天)'],
           df_dur_feq['总借入'],
           s=color.dot_size1,
           c=color.dot_color1,
           alpha=0.7)

ax.set_xlabel('平均借阅时间（天）')
ax.set_ylabel("总借入")
ax.set_title('')
ax.grid(True)

# ---------- 旋转 x 轴标签 ----------
plt.setp(ax.get_xticklabels(), rotation=45)

plt.tight_layout()  # 避免标签被截断
plt.show()