import seaborn as sns
import matplotlib.pyplot as plt
from flask import Blueprint, request, jsonify
from database import db
from bson import ObjectId
visualization_bp = Blueprint('visualization', __name__)
paper_collection = db.get_collection('clean_papers')
user_collection = db.get_collection('users')  # 假设这是用户表的集合

@visualization_bp.route('/paper', methods=['GET'])
def visualize_paper_stats(paper_id):
    # 从数据库查询论文数据
    # 这里使用示例数据，请根据实际需求修改查询条件
    papers = paper_collection.find({'_id': ObjectId(paper_id)})

    # 从查询结果中提取数据
    data = []
    for paper in papers:
        data.append([paper['citations'], paper['likes'], paper['views']])

    # 调用绘图函数
    labels = ['Number of Citations', 'Number of Likes', 'Number of Views']
    visualize_data(data, labels, 'Paper Statistics')


@visualization_bp.route('/author', methods=['GET'])
def visualize_author_stats(author_id):
    # 从数据库查询用户数据
    # 这里使用示例数据，请根据实际需求修改查询条件
    author_data = user_collection.find({'_id': ObjectId(author_id)})

    # 从查询结果中提取数据
    data = []
    for author in author_data:
        data.append([author['works'], author['follows'], author['views']])

    # 调用绘图函数
    labels = ['Number of Works', 'Number of Follows', 'Number of Views']
    visualize_data(data, labels, 'Author Statistics')

def visualize_data(data, labels, title):
    # 创建Seaborn的条形图
    sns.set(style="whitegrid")
    sns.set_color_codes("pastel")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=data, palette="Set3")

    # 添加标签
    plt.xlabel('Categories')
    plt.ylabel('Count')
    plt.title(title)

    # 显示图表
    plt.show()

# 调用函数生成图表
visualize_paper_stats()
visualize_author_stats()
