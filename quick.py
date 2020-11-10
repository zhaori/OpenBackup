import os
import time

from Lib.sqlite import Create_db
from config.db_config import *
from library import ha_hash, r_db_file


def _control(_path, filename):
    # st_atime(访问时间), st_mtime(修改时间), st_ctime（创建时间)
    suffer = os.path.join(_path, filename)
    c_time = os.stat(suffer).st_ctime
    m_time = os.stat(suffer).st_mtime
    f_hash = ha_hash(suffer)
    ctime = time.strftime('%Y.%m.%d.%X', time.localtime(c_time))
    mtime = time.strftime('%Y.%m.%d.%X', time.localtime(m_time))
    now_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    # 默认将文件大小为0的筛选出
    data_dict = {
        "file_path": _path,
        "file_name": os.path.join(_path, filename),
        "c_time": ctime,
        "x_time": mtime,
        "now_time": now_time,
        "file_hash": f_hash
    }
    # 这里返回的是dict格式的数据
    return data_dict


class quick(object):

    def __init__(self, table, mode, data, d_path=db_path):
        self.file_li = []  # 本地创建的文件列表
        self.table = table  # 表名
        self.mode = mode  # 建字段
        self.data = data  # 插入数据SQL语句
        self.db = Create_db(self.table, self.mode, self.data, d_path)

    def _len_file(self):
        # return:file_li number
        return len(self.file_li)

    def new_db(self):
        self.db.new_sql()

    def new_index(self, s_path):
        # 创建索引
        t = time.time()
        try:
            for root, file_p, filename in os.walk(s_path):
                if filename and root:
                    for name in filename:
                        self.db.add_sql(_control(root, name))
                        self.file_li.append(name)
            self.db.com_clone()
        except OSError:
            # 因为文件访问权限问题，不可能所有都能搜索，因此忽略掉这部分
            pass
        t2 = time.time()
        print(t2 - t)

    def search(self):
        # read_data = r_db_file()  # 从数据库里读取数据
        # file_list = r_db_file().r_list()  # 返回得到到的文件列表
        return r_db_file().r_list()


def x_x():
    import textwrap
    help_2 = textwrap.dedent("""\
            help:程序默认生成backup和data两个文件夹，前者是备份文件夹，后者是数据库文件存放位置可以在配置文件做修改
                1.  %s         2. %s
            """ % ("创建新数据库", "开始搜索"))

    return help_2


if __name__ == "__main__":

    def r_q():
        q = quick(db_table, db_mode, db_data)
        return q


    while 1:
        print(x_x())
        n = input('Please input your number:')

        if n == "1":
            if db_name not in os.listdir(data_path):
                r_q().new_db()
                print('数据库创建成功')
            else:
                print('数据库已存在，无需重复新建')

        elif n == "2":
            for p in search_path:
                r_q().new_index(p)
