from flask import Blueprint, request, jsonify
from database import db
import json
from bson import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
from utils.logger import logger

collection_bp = Blueprint('collection', __name__)

clean_papers_collection = db.get_collection('clean_papers')
authors_collection = db.get_collection('authors')
users_collection = db.get_collection('users')

# 路由用于获取用户收藏的作者和文献
@collection_bp.route('/collections/<user_id>', methods=['GET'])
def get_user_collections(user_id):

    # 查询 users 集合，找到用户的收藏信息
    user_data = users_collection.find_one({'_id': ObjectId(user_id)})

    if not user_data:
        return jsonify({'message': 'User not found'}), 404

    # 获取用户的收藏数组
    user_collections = user_data.get('collections', [])

    # 根据收藏数组中的 ObjectId 获取作者和文献信息
    authors = []
    papers = []

    for item_id in user_collections:
        author_data = authors_collection.find_one({'_id': ObjectId(item_id)})

        if author_data:
            author_data['_id'] = str(author_data['_id'])
            authors.append(author_data)
        else:
            paper_data = clean_papers_collection.find_one({'_id': ObjectId(item_id)})

            if paper_data:
                paper_data['_id'] = str(paper_data['_id'])
                for i in range(len(paper_data['*authors'])):
                    paper_data['*authors'][i] = str(paper_data['*authors'][i])
                if paper_data:
                    papers.append(paper_data)
            else:
                return jsonify({'message': 'User collections not found'}), 404

    logger.debug("collection/collections/%s : %s" % (user_id, authors))
    logger.debug("collection/collections/%s : %s" % (user_id, papers))
    # 返回用户的收藏信息
    return jsonify({
        'authors': authors,
        'papers': papers
    }), 200

@collection_bp.route('/user/collect', methods=['GET'])
def add_collection_to_user():
    # 获取用户的记录zz

    userid = request.args.get('userId')
    collection_id = request.args.get('collection_id')
    user_record = users_collection.find_one({'_id': ObjectId(userid)})
    # logger.debug("1")
    # logger.debug(userid)
    # logger.debug(collection_id)
    if user_record:
        # 获取当前的收藏集合
        current_collections = user_record.get('collections', [])

        # 检查 collection_id 是否已经在收藏集合中
        if collection_id in current_collections:
            logger.debug("/collection/user/collect : %s already added to user" % (collection_id))
            return jsonify({'message': 'Collection already added to user'}), 401
        
        # 将新的 collection_id 添加到收藏集合
        current_collections.append(collection_id)

        # 更新用户记录中的 collections 列
        users_collection.update_one(
            {'_id': ObjectId(userid)},
            {'$set': {'collections': current_collections}}
        )

        return jsonify({'message': 'Collection added to user'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


@collection_bp.route('/user/delete_collection', methods=['GET'])
def delete_collection_from_user():
    # 获取用户的记录zz

    userid = request.args.get('userId')
    collection_id=request.args.get('collection_id')
    user_record = users_collection.find_one({'_id': ObjectId(userid)})
    logger.debug("1")
    logger.debug(userid)
    logger.debug(collection_id)
    

    if user_record:
        # 获取当前的收藏集合
        current_collections = user_record.get('collections', [])

        # 删除collection_id
        if collection_id in current_collections:
            current_collections.remove(collection_id)
        else :
            return jsonify({'message': 'Collection is not exist'}), 401

        # 更新用户记录中的 collections 列
        users_collection.update_one(
            {'_id': ObjectId(userid)},
            {'$set': {'collections': current_collections}}
        )

        return jsonify({'message': 'Collection delete successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404