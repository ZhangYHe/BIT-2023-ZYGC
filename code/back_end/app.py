from flask import Flask
from auth.auth import auth_bp
from search.search import search_bp
from collection.collection import collection_bp
from information.information import information_bp
from admin.admin import admin_bp
from flask import Flask
from flask_cors import CORS
from database import db  # 导入数据库连接
import sys
print(sys.path)
app = Flask(__name__)
CORS(app)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(search_bp, url_prefix='/search')
app.register_blueprint(collection_bp, url_prefix='/collection')
app.register_blueprint(information_bp, url_prefix='/information')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
