import pymongo
from utils.logger import logger

class Database:
    def __init__(self, db_uri):
        try:
            self.client = pymongo.MongoClient(db_uri)
            self.db = self.client['Scholar']
            logger.info("Database connected !")
        except Exception as e:
            logger.info('Exception %s happened , Database connect error !' % e)

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def command(self, command):
        return self.db.command(command)

    def close(self):
        self.client.close()

# vultr服务器测试
db = Database("mongodb://admin:202309@64.176.214.218:27017/?authMechanism=DEFAULT")  # 使用你的 MongoDB 连接字符串
