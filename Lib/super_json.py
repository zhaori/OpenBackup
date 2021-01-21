import hashlib
import json
import os
import time

Data_Json = {
    "Python": {
        "OpenBackup":
            {
                "time": 20210119,
                "file": "OpenBackup01.7z",
                "url": "https://github.com/zhaori",
                "update": "https://zhaori.github.io//upload/OpenBackup/OpenBackup01.7z",
                "version": 0.1
            }
    }
}


def _get_log(err_name, error_data):
    err_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    with open(os.path.join('./Log', err_name), 'a', encoding="utf-8") as f:
        data = err_time + "   " + str(error_data)
        f.write(str(data) + "\n")


def get_sha256(s) -> str:
    return hashlib.sha256(str(s).encode('utf-8')).hexdigest()


def new_json(path):
    with open(os.path.join(path, "../update.json"), 'w', encoding='utf-8') as f:
        f.write(json.dumps(Data_Json, indent=4, ensure_ascii=False))


class SuperJSON(object):
    def __init__(self, json_file):
        self.json_file = json_file
        with open(self.json_file, 'r', encoding="utf-8") as f:
            self.data_json = dict(json.loads(f.read()))

    def _write(self):
        with open(self.json_file, 'w', encoding="utf-8") as f:
            f.write(json.dumps(self.data_json, indent=4, ensure_ascii=False))

    def dbs(self):
        """
        查询所有数据库
        """
        return [d for d in self.data_json.keys()]

    def tables(self, db):
        """
        查询数据库所有表
        """
        return [t for t in self.data_json[db].keys()]

    def field(self, db, table):
        """
        返回所有字段
        """
        return [t for t in self.data_json[db][table].keys()]

    def search_value(self, db, table, key):
        """
        返回值
        """
        return dict(self.data_json[db][table]).get(key)

    def insert(self, db, data: dict):
        """
        新增一条数据
        """
        self.data_json[db] = data
        self._write()

    def insert_all(self, db, data: list):
        """
        批量插入数据
        data: ["a":b{c:d}, "e": f{g:h}]
        """
        for i in data:
            self.data_json[db] = i

    def drop_db(self, db):
        del self.data_json[db]
        self._write()

    def drop_table(self, db, table):
        del self.data_json[db][table]
        self._write()

    def drop_value(self, db, table, key):
        del self.data_json[db][table][key]
        self._write()

    def upgrade(self, key, value):
        self.data_json[key] = value
        self._write()


if __name__ == '__main__':
    db = SuperJSON('../update.json')
    # db.drop_db('Rust', data="Hello")
    # print(db.search_key('Python', 'OpenBackup', 'version'))
