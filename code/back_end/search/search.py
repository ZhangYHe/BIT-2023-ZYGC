from bson import ObjectId
from flask import Blueprint, request, jsonify
from database import db
from utils.logger import logger

search_bp = Blueprint('search', __name__)
clean_papers_collection = db.get_collection('clean_papers')
authors_collection = db.get_collection('authors')
index_collection = db.get_collection('inverted_index_collection')
authors_inverted_collection = db.get_collection('authors_inverted_index_collection')
visualization_data = {}


# 路由用于执行关键词搜索
@search_bp.route('/searchres', methods=['GET'])
def search():
    visualization_data.clear()
    related_authors = 0
    year_data = [0, 0, 0, 0, 0, 0, 0, 0]
    keyword = request.args.get('keyword')
    logger.debug("/search/searchres get [ %s ]" % keyword)

    # # 在数据库中执行关键词搜索操作
    # # 你需要实现具体的搜索逻辑，使用 MongoDB 的查询或其他搜索引擎
    #
    # # 示例：使用 MongoDB 的基本搜索
    results_paper = index_collection.find_one({'keyword': keyword})
    results_author = authors_inverted_collection.find_one({'author_keyword': keyword})
    # 检查搜索结果是否为空
    if not results_paper and not results_author:
        logger.debug("/search/searchres get [ %s ] : No results found for the given query" % keyword)
        return jsonify({'message': 'No results found for the given query'}), 401

    # # 将结果中的文档 ID 收集到一个列表
    document_ids = []
    if results_paper:
        for i in results_paper['document_ids']:
            document_ids.append(str(i))
    # 查询visualization中的author
    if results_author:
        for i in results_author['document_ids']:
            document_ids.append(str(i))
        author_info = {
            'author_id': str(results_author['document_ids']),
            'name': results_author['author_keyword']
        }
        author_dict = {key: value for key, value in author_info.items()}
        visualization_data.update(author_dict)
    # 查询 index 集合以找到对应记录
    matching_records = []
    papernum = 0
    authornum = 0
    # 查询文献表
    for doc_id in document_ids:
        index_doc = clean_papers_collection.find_one({'_id': ObjectId(doc_id)})
        if index_doc:
            papernum += 1
            related_authors += len(index_doc['*authors'])
            index_doc['_id'] = str(index_doc['_id'])
            for i in index_doc['*authors']:
                i['id'] = str(i['id'])
            date = int(index_doc['*year'])
            if date < 1990:
                year_data[0] += 1
            elif 1990 <= date < 1995:
                year_data[1] += 1
            elif 1995 <= date < 2000:
                year_data[2] += 1
            elif 2000 <= date < 2005:
                year_data[3] += 1
            elif 2005 <= date < 2010:
                year_data[4] += 1
            elif 2010 <= date < 2015:
                year_data[5] += 1
            elif 2015 <= date < 2019:
                year_data[6] += 1
            elif 2019 <= date < 2024:
                year_data[7] += 1
            matching_records.append(index_doc)
    # 查询作者表
    for doc_id in document_ids:
        index_doc = authors_collection.find_one({'_id': ObjectId(doc_id)})
        if index_doc:
            authornum += 1
            index_doc['_id'] = str(index_doc['_id'])
            matching_records.append(index_doc)
    visualization_data['authornum'] = authornum
    visualization_data['papernum'] = papernum
    visualization_data['0-1990'] = year_data[0]
    visualization_data['1990-1995'] = year_data[1]
    visualization_data['1995-2000'] = year_data[2]
    visualization_data['2000-2005'] = year_data[3]
    visualization_data['2005-2010'] = year_data[4]
    visualization_data['2010-2015'] = year_data[5]
    visualization_data['2015-2019'] = year_data[6]
    visualization_data['2020-2024'] = year_data[7]
    visualization_data['related_authors'] = related_authors
    # "0-1990", "1990-1995", "1995-2000", "2000-2005", "2005-2010", "2010-2015", "2015-2019", "2020-2024"
    print(matching_records)

    return jsonify(matching_records)


@search_bp.route('/search_visualization', methods=['GET'])
def visualize_searchres_stats():
    return jsonify(visualization_data), 200
