from bson import ObjectId
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
#<<<<<<< wyz
    keyword = request.args.get('keyword')
    
    logger.debug("/search/searchres get [ %s ]" % keyword)

    # # 在数据库中执行关键词搜索操作
    # # 你需要实现具体的搜索逻辑，使用 MongoDB 的查询或其他搜索引擎
    #
    # # 示例：使用 MongoDB 的基本搜索
    results_paper = index_collection.find_one({'keyword': keyword})
    # # 将结果中的文档 ID 收集到一个列表
    document_ids = []
    if results_paper:
        for i in results_paper['document_ids']:
            document_ids.append(str(i))
    # 查询 index 集合以找到对应记录
    matching_records = []
    papernum = 0
    authornum = 0
    # 查询文献表
    for doc_id in document_ids:
        index_doc = clean_papers_collection.find_one({'_id': ObjectId(doc_id)})
        if index_doc:
            papernum += 1
            index_doc['_id'] = str(index_doc['_id'])
            for i in index_doc['*authors']:
                i['id'] = str(i['id'])
            matching_records.append(index_doc)
    # 查询作者表
    for doc_id in document_ids:
        index_doc = authors_collection.find_one({'_id': ObjectId(doc_id)})
        if index_doc:
            authornum += 1
            index_doc['_id'] = str(index_doc['_id'])
            matching_records.append(index_doc)
    print(matching_records)

    return jsonify(matching_records)
