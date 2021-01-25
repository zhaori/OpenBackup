import os
from ctypes import windll
from threading import Thread
from tkinter.messagebox import showinfo

from Lib.MongoDBSever import Mongodb_server
from config.MongoDB_Config import *

windll.shell32.SetCurrentProcessExplicitAppUserModelID('version')

with open('version', 'r') as f:
    tk_title = f'OpenBackup{f.read()}'
LOGO = r'./main.ico'

BACKUP_PATH = r'.\backups'
TEMP_PATH = r".\Temp"

# 加载任务
mongodb = Mongodb_server(mongo_host, mongo_port)
try:
    READ_DB = str(
        mongodb.search_one('tasks', mongodb.search_table('select')[0],
                           {"_id": 0, 'folder': 1})['folder']).replace('/', '\\')
except Exception:
    READ_DB = '/'


def about_main():
    showinfo(tk_title, '        本程序使用GPL 3.0协议开源\n '
                       '      软件的诞生离不开以下开源软件的支持\n '
                       '                  @ Python3.7  \n '
                       '                        7z 压缩 \n '
                       '                        SQLite \n'
                       '                       MongoDB \n'
                       '                       Tkinter GUI  \n '
                       '                       OpenSSL  \n '
                       '                       Notepad2 \n'
                       ' https://github.com/zhaori/OpenBackup')


def read_help():
    os.system(r'.\Script\Notepad2.exe .\doc\help.txt')


def ssh_options():
    def open_config():
        os.system(r'.\Script\Notepad2.exe .\config\Net_Config.py')

    t = Thread(target=open_config)
    t.start()
