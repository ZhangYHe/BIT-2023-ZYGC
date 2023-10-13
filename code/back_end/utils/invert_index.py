import nltk
from nltk.corpus import stopwords
from collections import defaultdict
from database import db

# 获取集合
index_collection = db.get_collection('clean_papers')

# 下载停用词
nltk.download('stopwords')
nltk.download('punkt')

# 初始化NLTK停用词列表
stop_words = set(stopwords.words('english'))

# 初始化倒排索引
inverted_index = defaultdict(list)

# 获取文档内容并进行分词
documents = list(index_collection.find({}, {'*title': 1}))
for doc in documents[:20]:
    if '*title' in doc:
        document_id = doc['_id']
        text = doc['*title']
        words = nltk.word_tokenize(text)

        # 去除停用词
        filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

        # 创建倒排索引
        for term in filtered_words:
            inverted_index[term].append(document_id)

# 将倒排索引存储回MongoDB
inverted_index_collection = db.get_collection('inverted_index_collection')
inverted_index_collection.insert_one({'inverted_index': dict(inverted_index)})
