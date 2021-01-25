import json
import os
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo

from Lib.MongoDBSever import Mongodb_server
from Lib.time_json import file_json
from config.MongoDB_Config import *
from work.begin_calendar import begin_time
from work.end_calendar import end_time


# ---------------------创建计划任务--------------- #

def new_task():
    # 防止阻塞主进程
    # def begin_time():
    #    os.system('begin_calendar.exe')

    # def end_time():
    #    os.system('end_calendar.exe')
    begin_time()
    end_time()

    data = {
        'begin': file_json().read_time('begin'),
        'end': file_json().read_time('end'),
        'folder': str(askdirectory()),
    }

    data_json = eval(str(json.dumps(data)))
    Mongodb_server(mongo_host, mongo_port).insert('tasks', os.path.basename(data['folder']), data_json)

    showinfo('Super Backups', '任务生成成功')
    time_file = ['begin_time', 'end_time', 'time.json']
    for file in time_file:
        if os.path.isfile(file):
            os.remove(file)


if __name__ == '__main__':
    new_task()
    # db = Mongodb_server(mongo_host, mongo_port)
    # name = db.search_one("tasks", "文件资源管理器", {"_id": 0, "begin": 1, "end": 1, 'folder': 1})
    # print(name['folder'])
