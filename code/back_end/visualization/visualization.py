# import seaborn as sns
# import matplotlib.pyplot as plt
from flask import Blueprint, request, jsonify
from database import db
from bson import ObjectId
from utils.logger import logger
import json

visualization_bp = Blueprint('visualization', __name__)
paper_collection = db.get_collection('clean_papers')
user_collection = db.get_collection('users')
visualize_collection = db.get_collection('visualize')
authors_collection = db.get_collection('authors')
search_collection = db.get_collection('inverted_index_collection')


@visualization_bp.route('/paper/<paper_id>', methods=['GET'])
def visualize_paper_stats(paper_id):
    if paper_id is None:
        return jsonify({'message': 'Missing paper_id parameter'}), 400

    # 在 clean_papers 表中查找具有相同 paper_id 的记录
    paper = paper_collection.find_one({'_id': ObjectId(paper_id)})

    if paper is None:
        return jsonify({'message': 'Paper not found'}), 404

    # 获取 paper 中的前三个作者的 author_id
    author_ids = [author['id'] for author in paper['*authors'][:3]]

    author_info = []

    for author_id in author_ids:
        # 在 visualize 表中查找相同 author_id 的记录
        author_record = visualize_collection.find_one({'author_id': author_id})

        if author_record:
            author_info.append({
                'paper_count': [period['paper_count'] for period in author_record['publication_periods']],
                'author_id': str(author_record['author_id']),
                'name': author_record['name']
            })
        else:
            author_info.append({
                'paper_count': [0, 0, 0, 0, 0, 0, 0, 0],
                'author_id': str(author_id),
                'name': 'Unknown'
            })

        # 如果需要填充缺失的作者信息
    while len(author_info) < 3:
        author_info.append({
            'paper_count': 0,
            'author_id': "",  # 或设置为其他默认值
            'name': 'Unknown'  # 或设置为其他默认值
        })

    logger.debug("/paper/%s : %s" % (paper_id, author_info))
    return jsonify(author_info), 200

    # '''
    # # 发送图片
    # # 从数据库查询论文数据
    # # 这里使用示例数据，请根据实际需求修改查询条件
    # papers = paper_collection.find({'_id': ObjectId(paper_id)})
    #
    # # 从查询结果中提取数据
    # data = []
    # for paper in papers:
    #     data.append([paper['citations'], paper['likes'], paper['views']])
    #
    # # 调用绘图函数
    # labels = ['Number of Citations', 'Number of Likes', 'Number of Views']
    # visualize_data(data, labels, 'Paper Statistics')
    # '''


@visualization_bp.route('/author/<author_id>', methods=['GET'])
def visualize_author_stats(author_id):
    if author_id is None:
        return jsonify({'message': 'Missing author_id parameter'}), 400

    # 在 visualize 表中查找具有相同 author_id 的记录
    author_record = visualize_collection.find_one({'author_id': ObjectId(author_id)})

    if author_record:
        # 获取 author_record 中的 publication_periods 信息
        publication_periods = author_record['publication_periods']
        author_info = {
            'paper_count': [period['paper_count'] for period in publication_periods],
            'author_id': str(author_record['author_id']),
            'name': author_record['name']
        }
    else:
        # 如果记录不存在，返回默认值
        author_info = {
            'paper_count': [0] * 8,
            'author_id': str(author_id),
            'name': 'Unknown'
        }

    logger.debug("/author/%s : %s" % (author_id, author_info))
    return jsonify(author_info), 200


    # '''
    # # 发送图片
    # # 从数据库查询用户数据
    # # 这里使用示例数据，请根据实际需求修改查询条件
    # author_data = user_collection.find({'_id': ObjectId(author_id)})
    #
    # # 从查询结果中提取数据
    # data = []
    # for author in author_data:
    #     data.append([author['works'], author['follows'], author['views']])
    #
    # # 调用绘图函数
    # labels = ['Number of Works', 'Number of Follows', 'Number of Views']
    # visualize_data(data, labels, 'Author Statistics')
    # '''

# '''
# def visualize_data(data, labels, title):
#     # 创建Seaborn的条形图
#     sns.set(style="whitegrid")
#     sns.set_color_codes("pastel")
#     plt.figure(figsize=(10, 6))
#     sns.barplot(data=data, palette="Set3")
#
#     # 添加标签
#     plt.xlabel('Categories')
#     plt.ylabel('Count')
#     plt.title(title)
#
#     # 显示图表
#     plt.show()
#
# # 调用函数生成图表
# visualize_paper_stats()
# visualize_author_stats()
# '''
