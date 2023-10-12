from flask import Flask, request, jsonify
import pymongo
from bson.json_util import dumps

app = Flask(__name__)

# vultr服务器测试
client = pymongo.MongoClient("mongodb://admin:202309@64.176.214.218:27017/?authMechanism=DEFAULT")
db = client['Scholar']
users_collection = db['users']

# clean_papers_tb = db['clean_papers']
# authors_tb = db['authors']

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

# 注册路由
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    existing_user = users_collection.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    user = {'username': username, 'password': password}
    users_collection.insert_one(user)

    return jsonify({'message': 'User registered successfully'}), 200

# 登录路由
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = users_collection.find_one({'username': username})
    if not user or user['password'] != password:
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful'}), 200

if __name__ == '__main__':
    app.run(debug=True)
