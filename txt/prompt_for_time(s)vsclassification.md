编写py代码，从数据集导入"Classification"和"平均借阅时间(天)"和"总借入"项 制作每个书籍种类的平均借阅时间柱状图和每个书籍种类的总借入次数柱状图
Classification项包含以下分类:'Literature','Language','Social Sciences','Science','Mathematics', 'General / Misc'

在绘制图表前加入以下代码保证中文正常显示:
plt.rcParams['font.sans-serif'] = ['Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

数据集地址：
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果.csv'
df = pd.read_csv(file_path)

将输出图表保存至"../rendering/time(s)_for_classification.png"

保证代码正确性 可读性