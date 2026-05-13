import pandas as pd
import matplotlib.pyplot as plt
import color
# ---------- 读取 CSV ----------
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果.csv'
df = pd.read_csv(file_path)



df['pages_num'] = df["Pages"].str.extract(r'(\d+)')[0].astype('Int64')

df=df[df['pages_num'] > 50]
# ---------- 去掉 pages 为空的数据 ----------
df_clean = df.dropna(subset=['pages_num', '平均借阅时间(天)','总借入'])
df_clean['lend_time_sum']=df_clean["总借入"]*df_clean['平均借阅时间(天)']
print(df_clean['pages_num'], df_clean['lend_time_sum'],df_clean['平均借阅时间(天)'])



plt.rcParams['font.sans-serif'] = ['Heiti TC']  # macOS 系统自带
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示


# ---------- 绘制散点图 ----------

fig, (lend_duration_sum,lend_times) = plt.subplots(2,1,figsize=(8,10))


lend_duration_sum.scatter(df_clean['pages_num'], df_clean['lend_time_sum'],s=color.dot_size1,c=color.dot_color1)
lend_duration_sum.set_xlabel('Pages')
lend_duration_sum.set_ylabel('平均借阅时间(天)')
lend_duration_sum.set_title('书籍页数 vs 平均借阅时间散点图')
lend_duration_sum.grid(True)


lend_times.scatter(df_clean['pages_num'],df_clean['总借入'],s=color.dot_size1,c=color.dot_color1)
lend_times.set_xlabel('Pages')
lend_times.set_ylabel('总借入次数')
lend_times.grid(True)
lend_duration_sum.set_title('书籍页数 vs 总借入次数散点图')



plt.savefig('../rendering/pages_vs_times&pages_vs_duration.png')
plt.show()