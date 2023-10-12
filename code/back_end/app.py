from flask import Flask
from auth.auth import auth_bp
from search.search import search_bp
from database import db  # 导入数据库连接

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(search_bp, url_prefix='/search')

# # vultr服务器测试
# client = pymongo.MongoClient("mongodb://admin:202309@64.176.214.218:27017/?authMechanism=DEFAULT")
# db = client['Scholar']
# users_collection = db['users']

# clean_papers_tb = db['clean_papers']
# authors_tb = db['authors']

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
