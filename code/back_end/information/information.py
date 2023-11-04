from flask import Blueprint, request, jsonify
from database import db
import json
from bson import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
from utils.logger import logger

information_bp = Blueprint('information', __name__)

clean_papers_collection = db.get_collection('clean_papers')
authors_collection = db.get_collection('authors')
visualize_collection = db.get_collection('visualize')

# 展示学者主页
@information_bp.route('/authors/<author_id>', methods=['GET'])
def get_author_details(author_id):
    # 查询 authors 集合，找到学者的信息
    author_data = authors_collection.find_one({'_id': ObjectId(author_id)})

    if not author_data:
        return jsonify({'message': 'Author not found'}), 404

    # 将 ObjectId 转换为字符串
    author_data['_id'] = str(author_data['_id'])

    visualize_data = visualize_collection.find_one({'author_id': ObjectId(author_id)})

    if visualize_data:
        for period in visualize_data.get('publication_periods', []):
            if 'paper_ids' in period:
                paper_ids = period.get('paper_ids', [])
                period['paper_ids'] = [str(paper_id) for paper_id in period['paper_ids']]
                paper_titles = []

                for paper_id in paper_ids:
                    paper_info = clean_papers_collection.find_one({'_id': ObjectId(paper_id)})
                    if paper_info and '*title' in paper_info:
                        paper_titles.append(paper_info['*title'])

                #logger.debug(period['paper_ids'])
                paper_info_list = [{'paper_id': paper_id, 'paper_title': title} for paper_id, title in
                                   zip(period['paper_ids'], paper_titles)]
                period['paper_info'] = paper_info_list

        author_data['publication_periods'] = visualize_data['publication_periods']

    logger.debug("information/authors/%s : %s" % (author_id,author_data))
    # 返回学者的信息
    return jsonify(author_data), 200

# 展示论文主页
@information_bp.route('/papers/<paper_id>', methods=['GET'])
def get_paper_details(paper_id):
    # 查询 papers 集合，找到论文的信息
    paper_data = clean_papers_collection.find_one({'_id': ObjectId(paper_id)})

    if not paper_data:
        return jsonify({'message': 'Paper not found'}), 404

    # 将 ObjectId 转换为字符串
    paper_data['_id'] = str(paper_data['_id'])
    for i in range(len(paper_data['*authors'])):
        paper_data['*authors'][i]['id'] = str(paper_data['*authors'][i]['id'])

    logger.debug("information/papers/%s : %s" % (paper_id,paper_data))
    # 返回论文的信息
    return jsonify(paper_data), 200