编写代码，旨在爬取豆瓣网的书籍评分
要求：
读入提供的存有书籍的数据集，从"Title"字段读取书籍名称
为每本书爬取豆瓣网上该书的评分
在dataframe中添加新列，名为"Rating"，将评分存入该列
导出数据集到原地址

需要完善的反反爬策略，例如：
1️⃣ IP 与访问策略
代理轮换：使用代理池切换 IP，防止单 IP 被封
请求间隔随机化：模拟真实用户访问，随机延时（1~5 秒或更长）
分布式爬虫：通过多台机器分散访问负载
2️⃣ 浏览器与行为模拟
无头浏览器：Selenium、Playwright 或 Puppeteer 模拟完整浏览器操作
User-Agent & Headers 动态切换：随机切换浏览器标识、Referer、Cookie 等
行为模拟：滚动页面、随机点击、滑动，模拟真实用户操作
3️⃣ JavaScript 动态渲染
页面完全渲染：使用浏览器驱动或 headless 浏览器执行 JS
分析 API 请求：找到真实数据接口，直接抓取 JSON / CSV 等
减少浏览器指纹：去掉 WebDriver、navigator.webdriver 等标识
4️⃣ 数据获取策略
解析动态参数：分析网站 JS 逻辑生成参数，避免直接抓取静态 URL
数据解密 / 解码：处理 Base64 或简单加密数据（仅公开数据，不涉及版权内容）
缓存机制：避免重复请求同一资源，提高效率
5️⃣ 负载与容错策略
失败重试：请求失败时随机延迟后重试
错误日志记录：分析失败原因，调整策略
并发控制：限制同一时间并发请求数，避免触发防护


豆瓣网站:https://book.douban.com
搜索框标签(若需要用到): <input id="inp-query" name="search_text" size="22" maxlength="60" placeholder="书名、作者、ISBN" value="">
存有评分的标签:<strong class="ll rating_num " property="v:average"> 8.5 </strong>

数据集地址：
file_path = '/Users/zzyyio/PycharmProjects/25-26 2nd term MT3 for students/dataset/汇总结果.csv'
df = pd.read_csv(file_path)

保证代码可读性 正确性