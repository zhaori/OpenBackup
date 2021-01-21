# 增量备份
"""
只备份不同的数据，但当天的总备份量为 完全备份+以往每天的增量备份总数据
"""

import os
import shutil
from tkinter.messagebox import showinfo

from Lib.Pydos import sys_copy
from Lib.safety.Hash import Hash
from Lib.z7 import archive
from config.Differential_Config import time_folder
from config.Main_Config import READ_DB


def incremental_backup():
    basename_folder = os.path.basename(READ_DB)  # 不包含文件夹路径，只取文件夹名字
    temp_folder = r".\Temp"  # 临时文件夹

    new_backup = r'.\backups\incremental\{}\{}'.format(basename_folder, time_folder)  # 生成以日期命名的文件夹
    if os.path.exists(new_backup) is False:
        os.makedirs(new_backup)

    if not os.listdir(new_backup):  # 以最新的一次差异备份的备份文件做备份底包
        basename_folder = os.path.basename(READ_DB)  # 不包含文件夹路径，只取文件夹名字
        diff_backup = r'.\backups\TimeBackup\{}'.format(basename_folder)
        copy_file = os.listdir(diff_backup)[-1]
        filepath, file = os.path.split(copy_file)
        sys_copy(os.path.join(diff_backup, copy_file), r'.\backups\incremental\{}\{}'.format(basename_folder, file))

    # 将上一次备份的文件解压到临时文件夹中
    file_zip_path = r'.\backups\incremental\{}'.format(basename_folder)
    file_list = None
    root_folder = None
    for root, dirs, file in os.walk(file_zip_path):
        if root and file:
            file_list = file
            root_folder = root
    try:
        file_zip_file = file_list[-1]
    except TypeError:
        raise BaseException('无其他增量备份文件, 先运行 “第一次增量备份先运行此文件.py”')

    unzip = os.path.join(root_folder, file_zip_file)
    archive.unzip(unzip, temp_folder)

    old_file_list = []  # 完整备份原始文件
    old_path_list = []  # 完整备份原始文件夹
    old_file_hash_list = []  # 完整备份的文件哈希值列表
    for temp_root, temp_dirs, temp_file in os.walk(temp_folder):
        for name in temp_file:
            old_file_list.append(os.path.join(temp_root, name))
            old_file_hash_list.append(Hash(os.path.join(temp_root, name)).md5())

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
            add_data.append(new_file)

        # 新文件在旧文件列表中且新文件哈希值不存在旧文件哈希值列表中，判定文件被修改
        elif new_file in old_file_list and Hash(new_file).md5() not in old_file_hash_list:
            add_data.append(new_file)

        # 新文件不在旧文件列表中且哈希值在旧文件哈希值中，判定文件夹被重命名或被移动
        elif new_file not in old_file_list and Hash(new_file).md5() in old_file_hash_list:
            add_data.append(new_file)

        # 新文件不存在旧文件列表中，判定文件是新增
        elif new_file not in old_file_list:
            add_data.append(new_file)

    now_file_hash = [Hash(i).md5() for i in now_file_list]
    for old_file in old_file_list:
        if old_file not in now_file_list and Hash(old_file).md5() not in now_file_hash:
            # 如果旧文件不在新文件列表中，判断是被删除
            add_data.append(old_file)
            del_data.append(old_file)

    for _old in old_path_list:
        if _old not in now_folder_list:
            # 当老文件夹不在现在的文件夹，删除
            add_data.append(_old)
            del_data.append(_old)

    for _new in now_folder_list:
        # 这里是新文件不在老文件夹中的时候
        if _new not in old_path_list:
            add_data.append(_new)

    def find_child_folder(path, data):
        """
         #:param path: 绝对路径
         #:param data: 查询数据
         #:return: 返回指定文件夹的子目录相对路径
        """
        p = path[path.find(data):]
        return p[len(data) + 1: len(p)]

    for info in add_data:
        temp_file = os.path.join(temp_folder, find_child_folder(info, basename_folder))
        filepath, file = os.path.split(temp_file)
        if os.path.exists(filepath) is False:
            os.makedirs(filepath)
        if info not in os.listdir(temp_folder):  # 避免自己复制自己
            if os.path.isfile(info):
                sys_copy(info, temp_file)
            elif os.path.isdir(info):
                try:
                    shutil.copytree(info, temp_file)
                except FileExistsError:
                    pass

    #  解压完全备份文件,与增量备份合并
    # new_zip = archive(data_path, READ_DB)
    # file_7z = '{}/{}.7z'.format(data_path, basename_folder)
    # new_zip.unzip(file_7z, temp_folder)  # 解压到TEMP临时文件夹
    os.system(r'{} -mx5 -t7z a {} {}\* -mmt -sdel'.format('7z', '{}'.format(new_backup), temp_folder))
    os.system('rd {}'.format(new_backup))
    showinfo('提示', '备份成功')


if __name__ == '__main__':
    incremental_backup()
