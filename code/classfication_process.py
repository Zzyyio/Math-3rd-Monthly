import pandas as pd

# ---------- 文件路径 ----------
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果_g12.csv'

# ---------- 读取 CSV ----------
df = pd.read_csv(file_path)

# ---------- 映射表 ----------
# IB 分类映射
ib_map = {
    'IB-1-CH': 'Literature',
    'IB-2-E': 'Language',
    'IB-3-AS': 'Social Sciences',
    'IB-3-EB': 'Social Sciences',
    'IB-3-H': 'Social Sciences',
    'IB-4-BI': 'Science',
    'IB-4-CH': 'Science',
    'IB-4-PH': 'Science',
    'IB-4-SC': 'Science',
    'IB-5-M': 'Mathematics',
    'IB-7-R.B': 'General / Misc',
    'IB-7-TOK': 'General / Misc'
}

# 中文图书分类 CLC 映射
clc_map = {
    'I': 'Literature',
    'B': 'Social Sciences',
    'C': 'Social Sciences',
    'J': 'Arts',
    'K': 'Social Sciences',
    'D': 'Social Sciences',
    'F': 'Social Sciences',
    'O': 'Science',
    'N': 'Science',
    'R': 'Science',
    'S': 'Science',
    'Q': 'Science',
    'T': 'Science',
    'H': 'Language',
    'Z': 'General / Misc',
    'E': 'General / Misc',
    'G': 'General / Misc',
}

# DDC 映射函数
def map_ddc(ddc_code):
    try:
        num = float(ddc_code.split('.')[0])
        if 0 <= num < 100: return 'General / Misc'
        elif 100 <= num < 200: return 'Social Sciences'
        elif 200 <= num < 300: return 'Social Sciences'
        elif 300 <= num < 400: return 'Social Sciences'
        elif 400 <= num < 500: return 'Language'
        elif 500 <= num < 600: return 'Science'
        elif 600 <= num < 700: return 'Science'
        elif 700 <= num < 800: return 'Arts'
        elif 800 <= num < 900: return 'Literature'
        elif 900 <= num <= 999: return 'Social Sciences'
        else:
            return 'General / Misc'
    except:
        return 'General / Misc'


# ---------- 分类函数 ----------
def classify_book(class_num):
    class_num = str(class_num).strip()
    # 1. IB 分类
    if class_num.startswith('IB-'):
        # 去掉最后的“-数字”部分
        parts = class_num.rsplit('-', 1)
        ib_prefix = parts[0]
        if(ib_map.get(ib_prefix,'ge')=='ge'):
            print("fyc1foieahohfowe")
        return ib_map.get(ib_prefix, 'General / Misc')

    # 2. CLC 分类
    elif class_num[0].isalpha():
        if(clc_map.get(class_num[0],'ge')=='ge'):
            print("fCLCLCLCLLCLCLCLCCCCCowe")
        return clc_map.get(class_num[0], 'General / Misc')
    # 3. DDC 分类
    elif class_num[0].isdigit():
        return map_ddc(class_num)
    else:
        print("!!!!!!!!!!1")
        return 'General / Misc'

# ---------- 应用函数 ----------
df['Classification'] = df['Classification Number'].apply(classify_book)

# ---------- 保存 CSV ----------
df.to_csv(file_path, index=False)
print(f"已更新 '{file_path}'，新列 'Classification' 已添加。")