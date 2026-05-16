import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import color
pd.set_option('display.max_rows', None)
total_students = 250

df = pd.read_excel("/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/all.xlsx")

df = df[df['Circulation Type'].isin(["续借","外借"])]
df = df[df['Grade']=='IB24G10']
df["UserID"] = df["UserID"].astype(str)
user = df.groupby("UserID").size().reset_index(name="借阅数量").sort_values(by="借阅数量", ascending=False)
user = user.reset_index(drop=True)

# 从 df 中取每个用户的唯一年级
grades = df.groupby("UserID")['Grade'].first().reset_index()  # first() 假设每个用户只有一个年级

# 合并借阅数量和年级
user = pd.merge(user, grades, on="UserID")


print(user)
freq = user['借阅数量'].value_counts().sort_index()

percent = freq/total_students*100
print(percent)

# 把未借书的百分比加到 Series，索引为0

percent = pd.concat([pd.Series({0: 100-sum(percent)}), percent])
# 按借阅次数排序（横轴从0开始）
percent = percent.sort_index()
fig, ax = plt.subplots(figsize=(12, 8))

# ax.bar(user['UserID'],user["借阅数量"])
ax.bar(percent.index,percent,color=color.bar_color1)
ax.set_xlabel("Borrowing/Renewal Counts")
ax.set_ylabel("% of students")
ax.set_title("Distribution of Student Borrowing Frequency-G10")
plt.savefig("../rendering/borrow_counts_per_user_g10.png")
plt.show()