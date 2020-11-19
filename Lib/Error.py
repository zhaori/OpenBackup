import os
import time


class Data_Type_Error(Exception):
    def __init__(self, *args, **kwargs):
        pass

    def __str__(self):
        return 'The ca_info type is not str'


class File_NOT_Find(Exception):
    def __init__(self, *args, **kwargs):
        pass

    def __str__(self):
        return "The file not find"


class DB_existed(Exception):

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self):
        return 'The SQLite DB exited, not repeat create!'


class ZIP_ERROR(Exception):

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self):
        return 'zip error'


class get_log(object):

    def __init__(self, error_path, error_name):
        self.now_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        self.error_file = os.path.join(error_path, error_name)

    def save(self, data):
        with open(self.error_file, 'db_full', encoding="utf-8") as f:
            data = self.now_time + "   " + str(data)
            f.write(str(data) + "\n \n")

    def get_time(self):
        return self.now_time

    def clean(self, size=None, option=None):
        # 如果option选项打开，则判断文件大小，大于等于即清空日志内容
        if option is True:
            if os.path.getsize(self.error_file) >= size:
                with open('error.log', 'w') as e:
                    e.write('')  # 填充空白
        else:
            with open('error.log', 'w') as e:
                e.write('')


if __name__ == "__main__":
    pass
