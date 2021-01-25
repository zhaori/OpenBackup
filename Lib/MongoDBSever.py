import pymongo
from pymongo.errors import ServerSelectionTimeoutError


class MongodbNOTFoundTableERROR(Exception):

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self):
        return '未找到Mongodb数据库的表'


class Mongodb_server(object):
    def __init__(self, host, port):
        # url_info = 'mongodb://{}:{}@{}:{}/{}'.format(db_name, db_password, host, port, db)
        try:
            self.server = pymongo.MongoClient(host, port, serverSelectionTimeoutMS=3000, socketTimeoutMS=3000)
        except ServerSelectionTimeoutError:
            pass

    def insert(self, db, table, data):
        """
        :return: 插入单个数据
        """
        try:
            db_table = self.server[db][table]
            db_table.insert_one(data)
        except ValueError:
            raise ValueError
        finally:
            self.server.close()

    def insert_list(self, db, table, data):
        """
        :param db: 数据库名称
        :param table:表名
        :param data:数据
        :return: 插入多条数据，以列表或者元组形式可迭代
        """
        try:
            db_table = self.server[db][table]
            db_table.insert(data.copy())
        except ValueError:
            raise ValueError
        finally:
            self.server.close()

    def search(self, db, table, key) -> list:
        """
        :param key: 格式例如：{"_id": 0, "username": 1},0为不查询，1为查询
        :return:
        """
        db_table = self.server[db][table]
        return [k for k in db_table.find({}, key)]

    def search_one(self, db, table, key):
        try:
            return self.server[db][table].find_one({}, key)
        except TypeError:
            return None

    def search_table(self, db) -> list:
        # 返回集合名的列表
        try:
            return self.server[db].list_collection_names()
        except ServerSelectionTimeoutError or TypeError:
            pass

    def update(self, db, table, old, new):
        """
        old = {"username": "皮得狠1", "phone": "123456"}
        new = {"$set": {"username": "皮得狠1", "phone": "123456789"}}
        mycol.update_many(old, new)
        """
        db_table = self.server[db][table]
        db_table.update_many(old, new)
        self.server.close()

    def del_key(self, db, table, data: dict):
        try:
            self.server[db][table].delete_many(data)
        except Exception as e:
            raise e
        finally:
            self.server.close()

    def del_table(self, db):
        # 删除表
        table_list = self.search_table(db)
        if table_list:
            for t in table_list:
                self.server[db][t].drop()
            self.server.close()
        else:
            raise MongodbNOTFoundTableERROR


if __name__ == "__main__":
    """
    data = {
        'username': 'pdh666',
        'lognpwd': ha_hash('666666'),
        'phone': '135xxxxxxx0410',
        'wx': '135xxxxxxx0410',
        'email': '1471584500',
        'address': '下一站都市B座313',
        'True_information': {
            'name': '皮得狠',
            'gender': '男',
            'age': '21',
            'nationality': '中华人民共和国',
            'ethnic_group': '汉',
            'id_address': ha_hash('四川省南充市'),
            'Identity_number': ha_hash('5113211xxxxxxx77100')

        }

    }
    """
    from config.MongoDB_Config import mongo_host, mongo_port

    db = Mongodb_server(mongo_host, mongo_port)
    # name = db.search_one("tasks", "文件资源管理器", {"_id": 0, 'folder': 1})
    # print(db.search_set('tasks'))
