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

# 管理员管理数据
@admin_bp.route('/data-management/<username>', methods=['POST'])
def admin_data_management(username):
    admin_token = request.headers.get('Authorization')

    # 验证管理员登录令牌
    if validate_admin_token(admin_token, username):
        try:
            data = request.get_json()

            # 确保 JSON 数据包含一个有效的 MongoDB 操作指令
            if 'mongo_command' in data:
                command = data['mongo_command']
                logger.debug("/admin/data-management/<username> : %s" % command)
                operation_type = command.get('operation_type')

                if operation_type == 'delete':
                    handle_delete_command(command)
                elif operation_type == 'insert':
                    handle_insert_command(command)
                elif operation_type == 'modify':
                    handle_modify_command(command)
                else:
                    return jsonify({'message': 'Invalid operation_type.'}), 400

                return jsonify({'message': 'Operation successful'}), 200
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
    if validate_admin_token(admin_token, username):
        try:
            data = request.get_json()

            # 确保 JSON 数据包含一个有效的 MongoDB 操作指令
            if 'mongo_command' in data:
                command = data['mongo_command']
                logger.debug("/admin/user-management/<username> : %s" % command)
                operation_type = command.get('operation_type')

                if operation_type == 'delete':
                    handle_delete_command(command)
                elif operation_type == 'insert':
                    handle_insert_command(command)
                elif operation_type == 'modify':
                    handle_modify_command(command)
                else:
                    return jsonify({'message': 'Invalid operation_type.'}), 400

                return jsonify({'message': 'Operation successful'}), 200
            else:
                return jsonify({'message': 'Invalid JSON data. Missing "mongo_command" field.'}), 400
        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Unauthorized'}), 401
    

def handle_delete_command(command):
    collection_name = command['delete']['collection']
    object_id = command['delete']['object_id']

    if collection_name and object_id:
        # 删除指定 collection 中的记录
        db.get_collection(collection_name).delete_one({'_id': ObjectId(object_id)})

        # 检查并删除收藏的记录
        if collection_name == 'clean_papers' or collection_name == 'authors':
            update_users_collections(object_id)

def update_users_collections(deleted_object_id):
    # 删除users表中收藏的记录
    users_collection.update_many(
        {"collections": deleted_object_id},
        {"$pull": {"collections": deleted_object_id}}   
    )

def handle_insert_command(command):
    collection_name = command['insert']['collection']
    documents = command['insert']['documents']

    if collection_name and documents:
        # 在指定 collection 中插入新记录
        db.get_collection(collection_name).insert_many(documents)

def handle_modify_command(command):
    try:
        collection_name = command['modify']['collection']
        query = command['modify']['query']
        update = command['modify']['update']

        if collection_name and query and update:
            # 更新指定 collection 中的记录
            db.get_collection(collection_name).update_many(query, update)
    except Exception as e:
        logger.error(f'/admin/data-management/<username> Error: {str(e)}')