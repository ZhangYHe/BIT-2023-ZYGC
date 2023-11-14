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
    email = data['email']

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    existing_user = users_collection.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    user = {'username': username, 'password': password, 'email': email, 'intro': '', 'is_admin': False}
    users_collection.insert_one(user)

    return jsonify({'message': 'User registered successfully'}), 200

@auth_bp.route('/password', methods=['POST'])
def changepassword():
    data = request.get_json()
    username = data['username']
    password = data['password']
    newpassword = data['newpassword']
    email = data['email']
    intro = data['intro']
    if not username:
        return jsonify({'message': 'Not login User!'}), 402
    user = users_collection.find_one({'username': username})
    if newpassword:
        if not password:
            return jsonify({'message': 'Password are required!'}), 400
        if user['password'] != password:
            return jsonify({'message': 'Please input correct password!'}), 401
        users_collection.update_one({'_id': user['_id']}, {'$set': {'password': newpassword, 'email': email, 'intro': intro}})
        return jsonify({'message': 'Password changed successfully!'}), 200
    else:
        users_collection.update_one({'_id': user['_id']}, {'$set': {'email': email, 'intro': intro}})
        return jsonify({'message': 'Information changed successfully!'}), 200

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
        return jsonify({'message': 'Admin login successful', 'admin_token': admin_token, 'email': user.get('email'), 'intro':user.get('intro'), 'user_id': user_id}), 200
    # 用户登录
    else:
        return jsonify({'message': 'User login successful', 'email': user.get('email'), 'intro':user.get('intro'), 'user_id': user_id}), 200
