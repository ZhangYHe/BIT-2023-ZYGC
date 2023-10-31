from flask import Blueprint, request, jsonify
from database import db
import json
from bson import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
import hashlib
import time
from utils.logger import logger

admin_bp = Blueprint('admin', __name__)

clean_papers_collection = db.get_collection('clean_papers')
authors_collection = db.get_collection('authors')
users_collection = db.get_collection('users')
crawl_collection = db.get_collection('crawl_tasks')

# 固定的秘密密钥，此密钥必须保密
SECRET_KEY = "your_secret_key"

def generate_admin_token(username):
    data = f'{username}{SECRET_KEY}'
    token = hashlib.sha256(data.encode()).hexdigest()
    return token

def validate_admin_token(token, username):
    expected_token = generate_admin_token(username)
    return token == expected_token

# 管理员登陆
@admin_bp.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data['admin_username']
    password = data['admin_password']

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = users_collection.find_one({'username': username})
    if not user or user['password'] != password:
        return jsonify({'message': 'Invalid credentials'}), 401

    if user['is_admin'] != True:
        return jsonify({'message': 'Not admin'}), 500

    # generate admin token
    admin_token = generate_admin_token(username)

    return jsonify({'message': 'Login successful', 'admin_token': admin_token}), 200

# 管理员管理数据 TODO 删除数据后更新用户收藏
@admin_bp.route('/data-management/<username>', methods=['POST'])
def admin_data_management(username):

    admin_token = request.headers.get('Authorization')

    # 验证管理员登录令牌
    if validate_admin_token(admin_token,username):
        try:
            data = request.get_json()

            # TODO 未测试，可能有问题
            # 确保 JSON 数据包含一个有效的 MongoDB 操作指令
            if 'mongo_command' in data:
                command = data['mongo_command']

                if 'delete' in command:  # 如果指令是删除数据
                    collection = command['delete']['collection']
                    object_id = command['delete']['object_id']

                    if collection and object_id:
                        # 在 users 表的 collection 中查找相同 objectid 的记录
                        user_collection.delete_one({'collection.item_id': object_id, 'collection.collection_type': collection})

                result = db.command(command)

                return jsonify({'message': 'Operation successful', 'result': result}), 200
            else:
                return jsonify({'message': 'Invalid JSON data. Missing "mongo_command" field.'}), 400
        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Unauthorized'}), 401

# 管理员管理爬虫任务
@admin_bp.route('/set-crawler/<username>', methods=['POST'])
def set_crawl_parameters(username):
    admin_token = request.headers.get('Authorization')

    # 验证管理员登录令牌
    if validate_admin_token(admin_token,username):
        try:
            data = request.get_json()

            # 确保 JSON 数据包含有效的爬虫参数
            if 'name' in data and 'target_url' in data and 'schedule' in data and 'crawl_rules' in data:
                crawling_task = {
                    'name': data['name'],
                    'target_url': data['target_url'],
                    'schedule': data['schedule'],
                    'crawl_rules': data['crawl_rules'],
                }

                # 插入数据到 crawling_tasks 集合
                result = crawl_collection.insert_one(crawling_task)

                return jsonify(
                    {'message': 'Crawl parameters set successfully', 'task_id': str(result.inserted_id)}), 200
            else:
                return jsonify({'message': 'Invalid JSON data. Missing required fields.'}), 400
        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Unauthorized'}), 401

# 管理员管理用户
@admin_bp.route('/user-management/<username>', methods=['POST'])
def admin_user_management(username):
    admin_token = request.headers.get('Authorization')

    # 验证管理员登录令牌
    if validate_admin_token(admin_token,username):
        try:
            data = request.get_json()

            # 确保 JSON 数据包含一个有效的 MongoDB 操作指令
            if 'mongo_command' in data:
                command = data['mongo_command']
                result = db.command(command)

                return jsonify({'message': 'Operation successful', 'result': result}), 200
            else:
                return jsonify({'message': 'Invalid JSON data. Missing "mongo_command" field.'}), 400
        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Unauthorized'}), 401