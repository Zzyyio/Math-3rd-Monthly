编写py代码，从数据集导入"rating"和"平均借阅时间(天)"和"总借入"项 制作每本书的rating和平均借阅时间散点图和每本书的rating和总借入次数散点图


在绘制图表前加入以下代码保证中文正常显示:
plt.rcParams['font.sans-serif'] = ['Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

数据集地址：
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果_with_rating_classification.csv'
df = pd.read_csv(file_path)

将输出图表保存至"../rendering/time(s)_vs_rating.png"

保证代码正确性 可读性