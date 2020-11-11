# 完全备份
import os
from sqlite3 import OperationalError
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, showerror
from Lib.json_py import PyJson
from Lib.safety.hash import Hash
from Lib.z7 import archive
from config.db_config import db_table, db_data, db_mode, data_path
from quick import quick


def full_backup():
    open_file = askopenfilename(title='打开任务文件', filetypes=([('任务文件json', '.json')]))
    p_j = PyJson(open_file)
    folder = p_j.read('folder')  # 全路径
    folder_file = os.path.basename(folder)  # 截取全路径最后一个反斜杠，可以是文件夹或文件
    if not os.path.exists('backups'):
        os.mkdir('backups')

    new_zip = archive(data_path, folder)
    new_zip.seven_zip(folder_file)

    try:
        db_path = os.path.join(r'.\backups', '{}{}'.format(folder_file, '.db'))
        quick(db_table, db_mode, db_data, d_path=db_path).new_db()
    except OperationalError:
        # 数据库文件重复存在错误检测，如果已存在则忽略
        pass

    search_path = [folder]
    for p in search_path:
        quick(db_table, db_mode, db_data).new_index(p)
    try:
        h = Hash(r'{}\{}.7z'.format(data_path, folder_file))
        h.sava_hash(h.md5(), '.md5', data_path)
        showinfo('提示', '备份完成')
    except:
        showerror('警告', '备份失败\n可能与无读写权限有关')


if __name__ == "__main__":
    # full_backup()
    showerror('警告', '   备份失败\n可能无读写权限')
