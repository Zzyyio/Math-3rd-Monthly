
编写py代码
目标为：
创建新dataframe命名为book_info
存储每本书的信息
统计书籍的平均借阅时长和总借阅，续借次数
从数据表格"Title"获取书的"Collection Barcode"也就是书的id，和书名"Title"，判断其是否在book_info中出现过
若此书名无出现过 在book_info中添加改书名行并导入数据表格中该书的属性数据（	Title	ISBN	Price	Author	Publisher	Publication time	Place of Publication	Pages	Classification Number	） 初始化其book_info中"is_lended","borrow_counts","renewal_counts"列的参数
若此书名出现过但此id未出现过 说明这是同个书的另一本 请在book_info的那本书下添加一个新的id，新id与其他隶属于该书下的id共用该书的属性数据
用is_lended表示该书的借阅状态 1 为在遍历到该位置时该书处于借出状态;0 为未借出

通过比对该书的is_lended和遍历到该处时该书在数据表格中的"Circulation Type"列（包含“续借”，“借入”，“归还”三种情况），
得出该书新的is_lend状态，并更新其平均借阅时长 若出现is_lended为0但circulation type为归还的错误 将错误打印到控制台并跳过该条数据
更新其借阅次数，续借次数，借阅-续借次数和

从以下目录获取数据表格
df = pd.read_excel("/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/all.xlsx"
                   ,sheet_name="Sheet1")

将输出导出为excel 存储地址为/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/output_dataset/book_info.xlsx

!important{
保证可读性 正确性 严谨性
该代码旨在通过数据集处理出包含每本书原有信息，平均借阅时间，总借入，总续借，总借入和续借量的新数据集，
以上的实现思路可能并非最佳 正确 如果你确定你有更好的实现思路 可使用你自己的思路 但要注明你的方法
同Title书可能有多个本 体现为Collection Barcode的不同，将每本书的借入借出情况单独处理 不要混淆 最终将其合并得到该Title的书的平均借阅时间，总借入，总续借，总借入和续借量
}