from setting.MongoDB_Config import *
from Lib.MongoDBSever import Mongodb_server
from tkinter.messagebox import showinfo
from pymongo.errors import ServerSelectionTimeoutError
import os
from ctypes import windll

windll.shell32.SetCurrentProcessExplicitAppUserModelID('version')

tk_title = 'OpenBackup 0.1 beta'
logo = './应用.ico'

# 监听文件夹
listen_dir = [
    r"D:\OneDrive\Python\垃圾回收站\文件资源管理器",
]


def about_main():
    showinfo(tk_title, '        本程序遵守GPL 3.0协议开源\n '
                       '                 @ Python3.7  \n '
                       '                        Tkinter  \n '
                       '                       OpenSSL  \n '
                       '                            7z  \n '
                       ' https://github.com/zhaori/OpenBackup')


def read_help():
    os.system('Notepad2.exe .\help.txt')


global mongodb

# while 1:
try:
    mongodb = Mongodb_server(mongo_host, mongo_port)
except ServerSelectionTimeoutError:
    os.system(r'.\Script\Mongodb-Restart.exe')
try:
    read_db = mongodb.search_one('tasks', mongodb.search_table('select')[0], {"_id": 0, 'folder': 1})
    READ_DB = read_db['folder']
except IndexError or ServerSelectionTimeoutError:
    pass
    # READ_DB = None
#    time.sleep(2)
