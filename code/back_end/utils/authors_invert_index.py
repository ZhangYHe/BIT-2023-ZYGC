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




# 获取集合
index_collection = db.get_collection('authors')

# 下载停用词
nltk.download('stopwords')
nltk.download('punkt')

# 初始化NLTK停用词列表
stop_words = set(stopwords.words('english'))

# 初始化倒排索引
inverted_index = defaultdict(list)

# 获取文档内容并进行分词
documents = list(index_collection.find({}, {'name': 1}))
for doc in documents:
    if 'name' in doc:
        document_id = doc['_id']
        text = doc['name']
        words = nltk.word_tokenize(text)

        # 去除停用词
        filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

        # 创建倒排索引
        for term in filtered_words:

            inverted_index[term].append(document_id)

# 将倒排索引存储回MongoDB
inverted_index_collection = db.get_collection('authors_inverted_index_collection')
print(inverted_index)
for keyword in inverted_index.keys():
    # print(inverted_index[keyword])
    t=list(inverted_index[keyword])
    inverted_index_collection.insert_one({'author_keyword': keyword, 'document_ids': t})

# inverted_index_collection.insert_one({'inverted_index': dict(inverted_index)})



# from back_end.database import db
# from collections import defaultdict
#
# # 连接到 MongoDB，获取数据库集合
# index_collection = db.get_collection('clean_papers')
#
# # 加载分词文档
# with open('tokenized_text.txt', 'r', encoding='utf-8') as file:
#     tokenized_text = file.read()
#
# # 分词文本
# tokens = tokenized_text.split()
#
# # 初始化倒排索引
# inverted_index = defaultdict(list)
#
# # 遍历分词文本和文档ID
# for document_id, term in enumerate(tokens, 1):
#     term = term.lower()
#
#     # 创建倒排索引
#     inverted_index[term].append(document_id)
#
# # 将倒排索引存储回MongoDB
# inverted_index_collection = db.get_collection('inverted_index_collection')
#
# # 清空现有的倒排索引数据
# inverted_index_collection.delete_many({})
#
# # 存储新的倒排索引数据
# for keyword in inverted_index.keys():
#     t = list(inverted_index[keyword])
#     inverted_index_collection.insert_one({'keyword': keyword, 'document_ids': t})
#
# # 查询示例：查询包含特定词语的文档
# query_term = 'your_query_term'
#
# query_result = inverted_index_collection.find_one({'keyword': query_term})
#
# if query_result:
#     # 如果查询词在倒排索引中存在，获取相关的文档ID
#     document_ids = query_result['document_ids']
#     print(f'Documents containing "{query_term}": {document_ids}')
# else:
#     print(f'No documents found for query term "{query_term}"')