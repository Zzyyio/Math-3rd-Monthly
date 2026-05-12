import pandas as pd
import matplotlib.pyplot as plt
import color  # 假设 color.dot_size1, color.dot_color1 已定义
import re
from datetime import datetime

# ---------- 读取 CSV ----------
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果.csv'
df = pd.read_csv(file_path)


# ---------- 处理写作日期 ----------
def parse_publication_date(s):
    if pd.isna(s):
        return None
    # 取第一个出现的年份
    match = re.search(r'(\d{4})', s)
    if not match:
        return None
    year = int(match.group(1))

    # 查找月份和日
    month_day_match = re.search(r'(\d{4})[^\d]*(\d{1,2})[^\d]*(\d{1,2})?', s)
    if month_day_match:
        # 提取 month, day，若缺省则默认1
        month = int(month_day_match.group(2)) if month_day_match.group(2) else 1
        day = int(month_day_match.group(3)) if month_day_match.group(3) else 1
    else:
        month = 1
        day = 1
    try:
        return datetime(year, month, day)
    except:
        return datetime(year, 1, 1)


df['写作日期'] = df['Publication time'].astype(str).apply(parse_publication_date)

# ---------- 去掉缺失数据 ----------
df_clean = df.dropna(subset=['写作日期', '平均借阅时间(天)',"总借入"])
df_clean["lend_duration_sum"]=df_clean["总借入"]*df_clean["平均借阅时间(天)"]
# ---------- 按日期排序 ----------
df_clean = df_clean.sort_values('写作日期')







plt.rcParams['font.sans-serif'] = ['Heiti TC']  # macOS 系统自带
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示


# ---------- 绘制散点图 ----------
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df_clean['写作日期'],
           df_clean['lend_duration_sum'],
           s=color.dot_size1,
           c=color.dot_color1,
           alpha=0.7)

ax.set_xlabel('写作日期')
ax.set_ylabel("平均借阅时间（天）")
ax.set_title('写作日期 vs 平均借阅时间')
ax.grid(True)

# ---------- 旋转 x 轴标签 ----------
plt.setp(ax.get_xticklabels(), rotation=45)

plt.tight_layout()
plt.show()