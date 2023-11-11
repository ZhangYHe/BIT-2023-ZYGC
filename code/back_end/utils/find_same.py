import nltk
from nltk.corpus import stopwords
from collections import defaultdict
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
clean_papers_collection = db.get_collection('clean_papers')
authors_collection = db.get_collection('authors')
index_collection = db.get_collection('inverted_index_collection')
authors_inverted_collection = db.get_collection('authors_inverted_index_collection')

    # # 在数据库中执行关键词搜索操作
    # # 你需要实现具体的搜索逻辑，使用 MongoDB 的查询或其他搜索引擎
    #
    # # 示例：使用 MongoDB 的基本搜索
results_paper = list(index_collection.find({}, {'keyword': 1}))
results_author = list(authors_inverted_collection.find({}, {'author_keyword': 1}))
db.close()
    # 检查搜索结果是否为空
for doc in results_paper:
    for doc_2 in results_author:
        if str(doc['keyword'])==str(doc_2['author_keyword']):
            print(str(doc['keyword']))

