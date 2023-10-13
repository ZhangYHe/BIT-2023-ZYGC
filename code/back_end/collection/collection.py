from flask import Blueprint, request, jsonify
from database import db

collection_bp = Blueprint('collection', __name__)

user_collections_collection = db.get_collection('user_collections')
clean_papers_collection = db.get_collection('clean_papers')
authors_collection = db.get_collection('authors')
users_collection = db.get_collection('users')
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


@collection_bp.route('/user/collect', methods=['GET'])
def add_collection_to_user():
    # 获取用户的记录
    data = request.get_json()
    username=data['username']
    collection_id=data['collection_id']
    user_record = users_collection.find_one({'username': username})

    if user_record:
        # 获取当前的收藏集合
        current_collections = user_record.get('collections', [])

        # 将新的 collection_id 添加到收藏集合
        current_collections.append(collection_id)

        # 更新用户记录中的 collections 列
        users_collection.update_one(
            {'username': username},
            {'$set': {'collections': current_collections}}
        )

        return jsonify({'message': 'Collection added to user'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404
