from flask import Blueprint, request, jsonify
from database import db
from utils.logger import logger

search_bp = Blueprint('search', __name__)
clean_papers_collection = db.get_collection('clean_papers')
authors_collection = db.get_collection('authors')
index_collection = db.get_collection('inverted_index_collection')
'''下面是GPT给的模板代码'''


# 路由用于执行关键词搜索
@search_bp.route('/searchres', methods=['GET'])
def search():
    data = request.get_json()
    keyword = data['keyword']
    print(keyword)
    # 在数据库中执行关键词搜索操作
    # 你需要实现具体的搜索逻辑，使用 MongoDB 的查询或其他搜索引擎

    # 示例：使用 MongoDB 的基本搜索
    results_paper = clean_papers_collection.find({
        '$text': {'$search': keyword}
    })
    results_author = authors_collection.find({
        '$text': {'$search': keyword}
    })
    # 将结果中的文档 ID 收集到一个列表
    document_paper_ids = [result['_id'] for result in results_paper]
    document_author_ids = [result['_id'] for result in results_author]
    # 查询 index 集合以找到对应记录
    matching_records = []
    # 查询文献表
    for doc_id in document_paper_ids:
        index_doc = index_collection.find_one({'_id': doc_id})
        if index_doc:
            matching_records.append(index_doc)
    # 查询作者表
    for doc_id in document_author_ids:
        index_doc = index_collection.find_one({'_id': doc_id})
        if index_doc:
            matching_records.append(index_doc)

    test_records = []
    #test 文献数据
    for index_doc in index_collection:
        if index_doc:
            test_records.append(index_doc)
    #test 作者数据
    for index_doc in index_collection:
            if index_doc:
                test_records.append(index_doc)
    return  jsonify(test_records)
    # return jsonify(matching_records)

# 其他搜索相关的视图函数和逻辑可以在这个模块中添加
