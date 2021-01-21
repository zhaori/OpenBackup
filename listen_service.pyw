from watchdog.events import *
from watchdog.observers import Observer

from Lib.MongoDBSever import Mongodb_server
from config.Main_Config import READ_DB
from config.MongoDB_Config import mongo_host, mongo_port
from work.gettime import now_time


class FileEventHandler(FileSystemEventHandler):
    # 初始化方法，默认数据库的名称为 history，表为当前的时间
    def __init__(self):
        FileSystemEventHandler.__init__(self)
        self.db_name = "history"

    @staticmethod
    def __add_value(db, data):
        # 插入Mongodb的数据, insert 分别插入的是数据库、表、数据
        m_db = Mongodb_server(mongo_host, mongo_port)
        m_db.insert(db, now_time(), data)

    # 文件或文件夹移动
    def on_moved(self, event):
        if event.is_directory:
            data = {
                "handle": "移动",
                "src_folder": event.src_path,
                "destination": event.dest_path
            }
            self.__add_value(self.db_name, data)

        else:
            data = {
                "handle": "移动",
                "src_folder": event.src_path,
                "destination": event.dest_path
            }
            self.__add_value(self.db_name, data)

    # 创建文件或文件夹
    def on_created(self, event):
        if event.is_directory:
            data = {
                "handle": "创建",
                'src_folder': event.src_path
            }
            self.__add_value(self.db_name, data)

        else:
            data = {
                "handle": "创建",
                'src_folder': event.src_path
            }
            self.__add_value(self.db_name, data)

    # 删除文件或文件夹
    def on_deleted(self, event):
        if event.is_directory:
            data = {
                "handle": "删除",
                "src_folder": event.src_path
            }
            self.__add_value(self.db_name, data)

        else:
            data = {
                "handle": "删除",
                "src_folder": event.src_path
            }
            self.__add_value(self.db_name, data)

    # 修改文件或文件夹
    def on_modified(self, event):
        if event.is_directory:
            data = {
                "handle": "修改",
                "src_folder": event.src_path
            }
            self.__add_value(self.db_name, data)

        else:
            with open(event.src_path, 'rb') as f:
                file = f.read()
            data = {
                "handle": "修改",
                "src_folder": event.src_path,
                "file": file
            }
            self.__add_value(self.db_name, data)


def start_server(dis_dir):
    """
    :param dis_dir: 监听的文件夹列表
    :return: 服务持久运行
    """
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, dis_dir, True)
    try:
        observer.start()
    except OSError:
        raise WindowsError('系统无权限访问')
    observer.join()

"""
def start_process(n: list):
    process_list = [Thread(target=start_server, args=(i,)) for i in n]
    for s in process_list:
        s.start()
    for s in process_list:
        s.join()
"""

if __name__ == "__main__":
    start_server(READ_DB)

    """
    m_db = Mongodb_server("127.0.0.1", 27017)
    a = m_db.search("history", "202011181349", {"_id": 0, "history": 1, "handle": 1, "src_folder": 1, "file": 1})
    file_bytes = []
    file_path = []
    for i in a:
        file_bytes.append(i['file'])
        file_path.append(i["src_folder"])

    for i in range(0, len(file_bytes)):
        with open(file_path[int(i)], 'wb') as f:
            f.write(file_bytes[int(i)])

    # print(file_bytes[0])
    """
