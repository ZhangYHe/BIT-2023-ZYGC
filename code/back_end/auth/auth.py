from flask import Blueprint, request, jsonify
from database import db  # 导入数据库连接
from admin.admin import generate_admin_token,validate_admin_token
from utils.logger import logger

auth_bp = Blueprint('auth', __name__)
users_collection = db.get_collection('users')

# 注册路由
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    existing_user = users_collection.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    user = {'username': username, 'password': password, 'is_admin': False}
    users_collection.insert_one(user)

    return jsonify({'message': 'User registered successfully'}), 200

# 登录路由
@auth_bp.route('/login', methods=['POST'])
def login():

    # 下面为测试代码
    #return jsonify({'message': 'Login successful'}), 200
    #return jsonify({'message': 'Username and password are required'}), 400
    # 上面为测试代码

    data = request.get_json()

    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = users_collection.find_one({'username': username})
    if not user or user['password'] != password:
        return jsonify({'message': 'Invalid credentials'}), 401

    is_admin = user.get('is_admin', False)
    user_id = str(user['_id'])
    # 管理员登录
    if is_admin:
        # generate admin token
        admin_token = generate_admin_token(username)
        return jsonify({'message': 'Admin login successful', 'admin_token': admin_token, 'user_id': user_id}), 200
    # 用户登录
    else:
        return jsonify({'message': 'User login successful', 'user_id': user_id}), 200
