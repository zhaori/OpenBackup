import os
import time

from Lib.safety.Hash import Hash
from Lib.sqlite import Create_db, list_to_str
from config.DB_Config import *


class r_db_file(object):

    def __init__(self):
        self.db = Create_db(db_table, db_mode, db_data, path=None)
        self.db_li_path = self.db.search_sql('file_path, file_name')

    def get_file(self, find_str):
        # 得到文件所在路径
        for s in self.db_li_path:
            if s[1] == find_str:
                return os.path.join(s[0], s[1])

    def r_list(self):
        # 获取数据库里的所有文件名并以列表的形式返回
        return [list_to_str(f) for f in self.db.search_sql('file_name')]
        # for f in self.db.search_sql('file_name'):
        #    print(str(f).strip('()'))


def _control(_path, filename):
    # st_atime(访问时间), st_mtime(修改时间), st_ctime（创建时间)
    suffer = os.path.join(_path, filename)
    data_dict = {
        "file_path": _path,
        "file_name": os.path.join(_path, filename),
        "c_time": os.stat(suffer).st_ctime,
        "m_time": os.stat(suffer).st_mtime,
        "now_time": time.strftime('%Y%m%d%H%M', time.localtime(time.time())),
        "file_hash": Hash(suffer).md5()
    }
    # 这里返回的是dict格式的数据
    return data_dict


class quick(object):

    def __init__(self, table, mode, data, d_path):
        self.table = table  # 表名
        self.mode = mode  # 建字段
        self.data = data  # 插入数据SQL语句
        self.db = Create_db(self.table, self.mode, self.data, d_path)

    def new_db(self):
        self.db.new_sql()

    def new_index(self, s_path):
        # 插入数据
        t = time.time()
        try:
            for root, file_p, filename in os.walk(s_path):
                if filename and root:
                    for name in filename:
                        self.db.add_sql(_control(root, name))
                        # self.file_li.append(name)
            self.db.com_clone()
        except OSError:
            # 因为文件访问权限问题，不可能所有都能搜索，因此忽略掉这部分
            pass
        t2 = time.time()
        print(t2 - t)

    @staticmethod
    def search():
        return r_db_file().r_list()  # 返回得到到的文件列表


if __name__ == "__main__":
    pass
