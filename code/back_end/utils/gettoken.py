import nltk
from nltk.corpus import stopwords
import  pymongo

class Database:
    def __init__(self, db_uri):
        self.client = pymongo.MongoClient(db_uri)
        self.db = self.client['Scholar']

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def command(self, command):
        return self.db.command(command)

    def close(self):
        self.client.close()


# vultr服务器测试
db = Database("mongodb://admin:202309@64.176.214.218:27017/?authMechanism=DEFAULT")  # 使用你的 MongoDB 连接字符串

# 获取集合
index_collection = db.get_collection('clean_papers')
text_data = []

# 分页查询并处理数据
page_size = 10  # 每页的大小
page_number = 0  # 起始页号

while True:
    # 分页查询，跳过前面的页数，获取多个文档
    documents = index_collection.find({}, {'_id': 1}).skip(page_number * page_size).limit(page_size)

    if len(list(documents)) == 0 or page_number > 2:
        break  # 已经没有更多的文档了
    print(documents)
    for doc in documents:
        if '*title' in doc:
            text_data.append(doc['*title'])
            print(doc['*title'])

        if '*abstract' in doc:
            text_data.append(doc['*abstract'])
            print(doc['*abstract'])
    page_number += 1
# 打开一个本地文本文件以写入数据
with open('text_data.txt', 'w', encoding='utf-8') as file:
    for text in text_data:
        file.write(text + '\n')  # 将每个文本数据写入文件，每个文本一行

print(text_data)
# 现在text_data包含了每十个一组的*title和*abstract内容
