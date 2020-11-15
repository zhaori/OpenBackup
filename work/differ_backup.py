# 差异备份
import os
import shutil
import sqlite3
from tkinter import Tk, Button, Label
from tkinter.filedialog import askopenfilename

from Lib.Number_CN import num_cn
from Lib.json_py import PyJson
from Lib.sqlite import Create_db
from Lib.safety.hash import Hash
from config.Differential_config import df_db_mode, df_db_data, time_folder
from config.db_config import db_table, db_mode, db_data, db_path, windll, logo


def _backup():
    open_file = askopenfilename(title='打开任务文件', filetypes=([('任务文件json', '.json')]))
    p_j = PyJson(open_file)
    folder = p_j.read('folder')  # 全路径

    basename_folder = os.path.basename(folder)  # 不包含文件夹路径，只取文件夹名字

    new_backup = r'.\backups\TimeBackup\{}\{}'.format(basename_folder, time_folder)  # 生成以日期命名的文件夹
    if os.path.exists(new_backup) is False:
        os.makedirs(new_backup)

    db_raw = Create_db(db_table, db_mode, db_data, path=db_path).search_sql(
        'file_path, file_name, file_hash')  # 读取完整备份数据库
    df_db_table = num_cn(time_folder)
    diff_path = r'../backups/TimeBackup/Differential.db'  # 差异备份数据库

    diff_db = Create_db(df_db_table, df_db_mode, df_db_data, path=diff_path)

    try:
        diff_db.new_sql()
        # pass
    except sqlite3.OperationalError:
        pass

    path_list = []
    old_folder_list = []  # 完整备份原始文件
    old_path_list = []  # 完整备份原始文件夹
    old_file_hash_list = []  # 完整备份的文件哈希值列表

    for file in db_raw:
        data = {
            'path': file[0],
            'file': os.path.join(file[0], file[1]),
            'hash': file[2]
        }

        path_list.append(data['path'])
        old_folder = data['file'].replace('/', '\\')  # 从完整备份里读取的原始文件路径
        old_path = data['path'].replace('/', '\\')
        old_folder_list.append(old_folder)
        old_path_list.append(old_path)
        old_file_hash_list.append(data['hash'])

    now_file_list = []  # 现在的文件
    now_folder_list = []  # 现在的文件夹
    now_hash_list = []  # 现在的文件哈希值
    for root, basename, filename in os.walk(folder):
        for f in filename:
            now_file_list.append(os.path.join(root, f))
            now_hash_list.append(Hash(os.path.join(root, f)).md5())
        now_folder_list.append(root)

    class list_compare(object):
        """
        列表进行对比
        """

        def __init__(self, list_one, list_two):
            self.one = list_one
            self.two = list_two

        def one_two(self):
            # 列表1有，列表2没有
            return list(set(self.one).difference(set(self.two)))

        def two_one(self):
            return list(set(self.two).difference(set(self.one)))

    for old_hash, new_hash in zip(old_file_hash_list, now_hash_list):
        if old_hash == new_hash:
            print(old_hash)

    diff_db2 = Create_db(df_db_table, df_db_mode, df_db_data, path=diff_path)
    differ_info = list_compare(now_file_list, old_folder_list).one_two()
    differ_info.extend(list_compare(now_folder_list, old_path_list).one_two())
    for info in differ_info:
        data_data = {
            'difference': info,
            'now_time': time_folder
        }
        diff_db2.add_sql(data_data)
        if os.path.isfile(info):
            shutil.copy2(info, os.path.join(new_backup, os.path.basename(info)))

    diff_db2.com_clone()
    os.system(r'{} -mx5 -t7z a {} {} -mmt -sdel'.format('7z', '{}'.format(new_backup), new_backup))


def close():
    exit()


def differ_backup():
    win = Tk()  # 构造窗体
    windll.shell32.SetCurrentProcessExplicitAppUserModelID('version')  # 任务栏图标

    _title = '差异备份'
    width = 250
    height = 90
    win.title(_title)
    # win.iconbitmap(logo)

    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    aligner = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    win.geometry(aligner)
    Label(win, text='先完全备份再运行', font=('黑体', '14')).place(relx=0.18, rely=0.1, width=161, height=30)
    Button(win, text='选择任务文件', command=_backup).place(relx=0.12, rely=0.6, width=80, height=30)
    Button(win, text='退出', command=close).place(relx=0.52, rely=0.6, width=80, height=30)
    win.mainloop()


differ_backup()
