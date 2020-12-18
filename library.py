import os

from Lib.sqlite import Create_db, list_to_str
from setting.DB_Config import *


def filtrate(li, ignore_list):
    # 过滤无用文件及文件夹
    # 通过
    if ignore_list == "name":
        for i in ignore_file_name:
            while i in li:
                li.remove(i)
        return li

    elif ignore_list == "size":
        for file in li:
            if os.path.getsize(file) in ignore_file_size:
                while file in li:
                    li.remove(file)
        return li


# 第一步，从数据库获取表名，第二步获取表字段，第三部获取表数据


class r_db_file(object):

    def __init__(self):
        self.db = Create_db(db_table, db_mode, db_data, db_path)
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


class find_file(object):
    # 匹配查找列表里的文件
    def __init__(self, li):
        self._list = li
        self.filename = []
        self.suffix = []

    def f_name(self, name):
        # 按照文件名来查找
        for data in self._list:
            # find 查找到的会返回0，查找不到的会返回-1
            if data.find(name) == 0:
                self.filename.append(data)

        return self.filename

    def f_suffix(self, suffix):
        # 按照文件后缀名来搜索
        for data in self._list:
            # os.path.splitext 这个函数返回的是元祖的数字类型
            if os.path.splitext(data)[1] == suffix:
                self.suffix.append(data)

        return self.suffix

    def name_suffix(self, name, suffix):
        # 返回同时按照文件名模糊及后缀名精确搜索
        data_list = []
        for data in self._list:
            if data.find(name) == 0 and \
                    os.path.splitext(data)[1] == suffix:
                data_list.append(data)

        return data_list
