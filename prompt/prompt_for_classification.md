根据你上问的分类，编写py代码，根据数据集中的Classification Number项 获取其分类id
ib分类id格式为"IB-7-R.B-1","IB-1-CH-1"根据除最后一位-数字的其他信息判断类别
Chinese Library Classification格式为"I561.45","B84"根绝开头的字母判断类别
Dewey Decimal Classification and Relative Index的格式为"823.7","128" 根据数字判断列别
为dataframe新建一列 名为“Classification”:根据你上文的映射表将每本书的分类输出到此列
将output更新到input的filepath
不要修改数据集中的其他数据

file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果.csv'
df = pd.read_csv(file_path)