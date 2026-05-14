编写py代码，从数据集导入"Classification"和"平均借阅时间(天)"和"总借入"项 制作平均借阅时间(x)和classification(y)和总借入次数(z)的3d散点图 并用不同颜色表示不同的书的"Classification""

Classification项包含以下分类:'Literature','Language','Social Sciences','Science','Mathematics', 'General / Misc'

在绘制图表前加入以下代码保证中文正常显示:
plt.rcParams['font.sans-serif'] = ['Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

数据集地址：
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果_with_rating_classification.csv'
df = pd.read_csv(file_path)

将输出图表保存至"../rendering/class_vs_time_scatter.png"

保证代码正确性 可读性