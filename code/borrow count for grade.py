import pandas as pd

import matplotlib.pyplot as plt
import color
pd.set_option('display.max_rows', None)
total_students = 250

df = pd.read_excel("/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/all.xlsx")

df = df[df['Circulation Type'].isin(["续借","外借"])]
grade = df.groupby(["Grade","Circulation Type"]).size().unstack(fill_value=0)
grade = grade.sort_index(ascending=False)
print(grade)
fig, ax = plt.subplots(figsize=(12, 8))

# ax.bar(user['UserID'],user["借阅数量"])
ax.bar(grade.index,grade['外借'],color=color.bar_color1)
ax.bar(grade.index,grade['续借'],bottom=grade['外借'],color=color.bar_color2)
ax.set_xlabel("Grade")
ax.set_ylabel("Borrowing/Renewal Counts")
ax.set_title("Total Borrowing/Renewal Counts Per Grade")
plt.savefig("../rendering/Borrowing_Renewal_Counts_Per-Grade.png")
plt.show()