# chatbot-test
文件夹组织：
context：txt格式的微信数据
contexts：测试用的文件夹
json_data：政府网站json数据
wx_json：json格式的微信数据，补充了url和titile元信息，用于后面测试系统是否可以正确回答问题时，与retrieve的document的metadata对比用。
xxx/questions：在 `context` `json_data` `wx_json` 三个文件夹中的`questions`文件夹，都有生成的对应问题，
creep.py： 政府数据爬虫
generate_questions.py：生成问题的脚本
input.txt：微信公众号链接
wechat.py：爬取微信文章的爬虫（后续有考虑使用无格式爬取+利用大模型整理格式的方式实现）
