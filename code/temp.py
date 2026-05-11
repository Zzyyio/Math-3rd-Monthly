import numpy as np
import pandas as pd

df = pd.read_excel("/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/all.xlsx"
                   ,sheet_name="Sheet1")
list=[]
for name in df["Title"]:
    if name in list:
        continue
    list.append(name)
print(len(list))