from flask import Blueprint, request, jsonify
from database import db

collection_bp = Blueprint('collection', __name__)

user_collections_collection = db.get_collection('user_collections')
clean_papers_collection = db.get_collection('clean_papers')
authors_collection = db.get_collection('authors')

'''
{
  "user_id": "user123",
  "item_id": "paper456",
  "collection_type": "paper",
  "timestamp": "2023-10-12T08:00:00Z"
}

'''

# 路由用于获取用户收藏的作者和文献
@collection_bp.route('/user/collections/<user_id>', methods=['GET'])
def get_user_collections(user_id):
    # 查询 user_collections 集合，找到用户收藏的文献和作者
    user_collections = user_collections_collection.find({'user_id': user_id})

    # 根据 collection_type 区分文献和作者，并获取相关信息
    authors = []
    papers = []

    for collection in user_collections:
        item_id = collection['item_id']
        collection_type = collection['collection_type']

        if collection_type == 'author':
            author_data = authors_collection.find_one({'_id': item_id})
            if author_data:
                authors.append(author_data)
        elif collection_type == 'paper':
            paper_data = clean_papers_collection.find_one({'_id': item_id})
            if paper_data:
                papers.append(paper_data)

    # 返回用户的收藏信息
    return jsonify({
        'authors': authors,
        'papers': papers
    }), 200
