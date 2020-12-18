# 差异备份
import os
import shutil
import sqlite3
from tkinter.messagebox import showinfo

from Lib.Number_CN import num_cn
from Lib.PyDOS import sys_copy
from Lib.safety.Hash import Hash
from Lib.sqlite import Create_db
from Lib.z7 import archive
from setting.Main_Config import READ_DB
from setting.DB_Config import db_table, db_mode, db_data, db_path
from setting.Differential_Config import df_db_mode, df_db_data, time_folder


def differ_backup():
    basename_folder = os.path.basename(READ_DB)  # 不包含文件夹路径，只取文件夹名字

    new_backup = r'.\backups\TimeBackup\{}\{}'.format(basename_folder, time_folder)  # 生成以日期命名的文件夹
    if os.path.exists(new_backup) is False:
        os.makedirs(new_backup)

    db_raw = Create_db(db_table, db_mode, db_data, path=db_path).search_sql(
        'file_path, file_name, file_hash')  # 读取完整备份数据库
    df_db_table = num_cn(time_folder)
    diff_path = r'.\backups\TimeBackup\{}.db'.format(basename_folder)  # 差异备份数据库

    diff_db = Create_db(df_db_table, df_db_mode, df_db_data, path=diff_path)
    try:
        diff_db.new_sql()
        # pass
    except sqlite3.OperationalError:
        pass

    path_list = []
    data_dict_list = []  # 生成的数据库数据的列表
    old_file_list = []  # 完整备份原始文件
    old_path_list = []  # 完整备份原始文件夹
    old_file_hash_list = []  # 完整备份的文件哈希值列表

    for file in db_raw:
        data = {
            'path': file[0].replace('/', '\\'),
            'file': os.path.join(file[0], file[1]).replace('/', '\\'),
            'hash': str(file[2]).strip('\n')
        }
        data_dict_list.append(data)
        path_list.append(data['path'])
        old_folder = data['file'].replace('/', '\\')  # 从完整备份里读取的原始文件路径
        old_path = data['path'].replace('/', '\\')
        old_file_list.append(old_folder)
        old_path_list.append(old_path)
        old_file_hash_list.append(data['hash'])

    now_file_list = []  # 现在的文件
    now_folder_list = []  # 现在的文件夹
    for root, basename, filename in os.walk(READ_DB):
        for f in filename:
            now_file = os.path.join(root, f).replace('/', '\\')
            now_file_list.append(now_file)
        now_folder_list.append(root.replace('/', '\\'))

    # 通过验证哈希值的不同来判断文件是否已经修改
    # 验证文件哈希值，如果哈希值相同但名称不同，证明文件名被修改
    # 如果老文件与新文件都存在，但新文件哈希值不等于老文件哈希值，证明文件被修改过

    def hash_or_file(data):
        hash_file_dict = dict()  # 通过哈希值找寻源文件名
        for key, value in zip(old_file_hash_list, old_file_list):
            if data == 'hash':  # 通过哈希值返回文件
                hash_file_dict[key] = value
            elif data == 'file':
                hash_file_dict[value] = key
        return hash_file_dict

    add_data = []  # 提交到数据库的数据
    del_data = []  # 需要删除的数据
    for new_file in now_file_list:
        # 新文件不存在旧文件列表中且新文件的哈希值在旧文件哈希值列表中时，判定文件被重命名
        if new_file not in old_file_list and Hash(new_file).md5() in old_file_hash_list:
            _diff_data = {
                "mode": "rename",
                "difference": new_file,
                "source": hash_or_file('hash')[Hash(new_file).md5()],
                "reduce": "{}.7z".format(new_backup),
                "now_time": time_folder
            }
            add_data.append(_diff_data)

        # 新文件在旧文件列表中且新文件哈希值不存在旧文件哈希值列表中，判定文件被修改
        elif new_file in old_file_list and Hash(new_file).md5() not in old_file_hash_list:
            diff_data = {
                "mode": "modify",
                "difference": new_file,
                "source": new_file,
                "reduce": "{}.7z".format(new_backup),
                "now_time": time_folder
            }
            add_data.append(diff_data)

        # 新文件不在旧文件列表中且哈希值在旧文件哈希值中，判定文件夹被重命名或被移动
        elif new_file not in old_file_list and Hash(new_file).md5() in old_file_hash_list:
            diff_data = {
                "mode": "modify",
                "difference": new_file,
                "source": new_file,
                "reduce": "{}.7z".format(new_backup),
                "now_time": time_folder
            }
            add_data.append(diff_data)

        # 新文件不存在旧文件列表中，判定文件是新增
        elif new_file not in old_file_list:
            diff_data = {
                "mode": "add",
                "difference": new_file,
                "source": new_file,
                "reduce": "{}.7z".format(new_backup),
                "now_time": time_folder
            }
            add_data.append(diff_data)

    for old_file in old_file_list:
        if old_file not in now_file_list:
            # 如果旧文件不在新文件列表中，判断是被删除
            diff_data = {
                "mode": "del",
                "difference": old_file,
                "source": old_file,
                "reduce": "{}.7z".format(new_backup),
                "now_time": time_folder
            }
            add_data.append(diff_data)
            del_data.append(old_file)

    for _old in old_path_list:
        if _old not in now_folder_list:
            # 当老文件夹不在现在的文件夹，删除
            diff_data = {
                "mode": "del",
                "difference": _old,
                "source": _old,
                "reduce": "{}.7z".format(new_backup),
                "now_time": time_folder
            }
            add_data.append(diff_data)
            del_data.append(_old)

    for _new in now_folder_list:
        if _new not in old_path_list:
            diff_data = {
                "mode": "add",
                "difference": _new,
                "source": _new,
                "reduce": "{}.7z".format(new_backup),
                "now_time": time_folder
            }
            add_data.append(diff_data)

    temp_folder = r".\Temp"  # 临时文件夹
    data_path = r'.\backups'  # 备份文件夹

    def find_child_folder(path: str, data: str):
        """
        :param path: 绝对路径
        :param data: 查询数据
        :return: 返回指定文件夹的子目录相对路径
        """
        p = path[path.find(data):]
        return p[len(data) + 1: len(p)]

    diff_db2 = Create_db(df_db_table, df_db_mode, df_db_data, path=diff_path)
    #  解压完全备份文件与差异备份合并
    new_zip = archive(data_path, READ_DB)
    file_7z = '{}/{}.7z'.format(data_path, basename_folder)
    new_zip.unzip(file_7z, temp_folder)  # 解压到TEMP临时文件夹
    for info in add_data:
        temp_file = os.path.join(temp_folder, find_child_folder(info['difference'], basename_folder))
        filepath, file = os.path.split(temp_file)
        if os.path.exists(filepath) is False:
            os.makedirs(filepath)

        if os.path.isfile(info['difference']):
            sys_copy(info['difference'], temp_file)
        elif os.path.isdir(info['difference']):
            try:
                shutil.copytree(info['difference'], temp_file)
            except FileExistsError:
                pass

        diff_db2.add_sql(info)
    diff_db2.com_clone()

    for i in del_data:
        temp_file = os.path.join(temp_folder, find_child_folder(i, basename_folder))
        try:
            if os.path.isfile(temp_file):
                os.remove(temp_file)  # 删除文件
            elif os.path.isfile(temp_file) is False:
                shutil.rmtree(temp_file)  # 删除文件夹
        except FileNotFoundError:
            pass

    os.system(r'{} -mx5 -t7z a {} {}\* -mmt -sdel'.format('7z', '{}'.format(new_backup), temp_folder))
    os.system(f'rd {new_backup}')
    showinfo('提示', '备份成功')


if __name__ == '__main__':
    differ_backup()
