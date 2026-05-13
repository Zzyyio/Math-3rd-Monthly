import pandas as pd
import requests
import time
import random

# -------------------------------
# CSV 路径
# -------------------------------
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果.csv'
df = pd.read_csv(file_path)

# -------------------------------
# Open Library 查询函数
# -------------------------------
def get_openlibrary_rating(title, retries=3):
    """
    查询 Open Library 搜索 API，获取书籍星级评分
    返回 dict：{'average_rating': float, 'ratings_count': int, 'edition_count': int}
    """
    base_url = "https://openlibrary.org/search.json"
    for attempt in range(retries):
        try:
            params = {
                "q": title,
                "limit": 1,
                "fields": "title,ratings_average,ratings_count,edition_count"
            }
            response = requests.get(base_url, params=params, timeout=10)
            data = response.json()
            if data['numFound'] > 0:
                doc = data['docs'][0]
                return {
                    'average_rating': doc.get('ratings_average', None),
                    'ratings_count': doc.get('ratings_count', None),
                    'edition_count': doc.get('edition_count', None)
                }
            else:
                return {'average_rating': None, 'ratings_count': None, 'edition_count': None}
        except Exception as e:
            wait_time = random.uniform(1, 3)
            print(f"[Warning] 获取《{title}》失败，{attempt+1}/{retries} 重试，等待 {wait_time:.1f}s")
            time.sleep(wait_time)
    return {'average_rating': None, 'ratings_count': None, 'edition_count': None}

# -------------------------------
# 遍历 CSV 获取评分
# -------------------------------
avg_ratings = []
ratings_counts = []
edition_counts = []

for idx, row in df.iterrows():
    title = str(row['Title'])
    print(f"[Info] 查询书籍: {title} ({idx+1}/{len(df)})")
    rating_info = get_openlibrary_rating(title)
    avg_ratings.append(rating_info['average_rating'])
    ratings_counts.append(rating_info['ratings_count'])
    edition_counts.append(rating_info['edition_count'])
    print(rating_info)
    # 随机延时，模拟真实用户访问
    time.sleep(random.uniform(0.5, 1.5))

# -------------------------------
# 写回 CSV
# -------------------------------
df['Rating'] = avg_ratings
df['Ratings_Count'] = ratings_counts
df['Edition_Count'] = edition_counts

df.to_csv(file_path, index=False)
print(f"[Info] 查询完成，已保存到 {file_path}")