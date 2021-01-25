"""
Python version:3.7 x64
OS: Windows10 64
Pycharm version: 3.2
Github Index: https://github.com/zhaori
差异备份：设：y为当天备份总数据 z为当前新的数据，a为完整备份文件，x为当天。用！=表示两者差异部分的数据，表达式为下
y = a+(z!=(x-1))+(z!=x)
解释：除了首次备份，所有的备份都是用新数据与上次备份的数据进行比较，然后每次备份的数据只是当期比较的差异数据
例如：我有个文件夹存放的有a b c 三个元素，然后
第一天新增了 d 那么第一次开始差异备份 是 abc: d
第二天新增了e 那么第二次的差异备份是 abc: ed
第三天删除了a,那么第三次差异备份是 abc: bc+d+ed
"""
import os
import shutil
from tkinter.messagebox import showinfo

from Lib.Pydos import sys_copy, SYSTEM_TEMP
from Lib.safety.Hash import Hash
from Lib.sqlite import Create_db, list_to_str
from Lib.z7 import archive
from config.DB_Config import db_table, db_mode, db_data
from config.Main_Config import BACKUP_PATH, READ_DB, TEMP_PATH
from work.gettime import now_time


def original_file():
    # 用一份完全备份包作为底包，意味着一切备份的依据都是这个
    basename_folder = os.path.basename(READ_DB)  # 不包含文件夹路径，只取文件夹名字
    copy_full = os.path.join(fr'.\backups\TimeBackup\{basename_folder}', f"{basename_folder}.7z")
    full_backup = os.path.abspath(os.path.join(BACKUP_PATH, f"{basename_folder}.7z"))  # 完全备份压缩包的相对路径
    full_backup_db = os.path.abspath(os.path.join(BACKUP_PATH, f"{basename_folder}.db"))  # 完全备份压缩包的相对路径
    copy_full_db = os.path.join(fr'.\backups\TimeBackup\{basename_folder}', f"{basename_folder}.db")
    return [copy_full, full_backup, full_backup_db, copy_full_db]


def copy_ready():
    # 把完全备份文件拷贝到增量备份文件夹里作为备份的依据
    sys_copy(original_file()[1], original_file()[0])
    sys_copy(original_file()[2], original_file()[3])


def unzip_backup():
    # 将底包解压到临时文件夹总，然后与现存文件夹的内容进行对比
    archive.unzip(original_file()[0], TEMP_PATH)


def find_child_folder(path: str, data: str):
    """
    :param path: 绝对路径
    :param data: 查询数据
    :return: 返回指定文件夹的子目录相对路径
    """
    p = path[path.find(data):]
    return p[len(data) + 1: len(p)]


old_file_list = []  # 原始完整备份的文件
old_folder_list = []  # 原始完整备份的文件夹
old_dict = dict()  # 旧文件哈希值字典
new_file_list = []  # 最新文件
new_folder_list = []  # 最新文件夹
new_dict = dict()  # 新文件哈希值字典
add_backup = []  # 添加入备份的集合，用现存数据与原始备份数据对比得到的
del_backup = []  # 删除文件/文件夹的集合，是用原始备份数据对比现存数据得到的


def differential_backup():
    # if original_file()[0] not in os.listdir(fr'.\backups\TimeBackup\{os.path.basename(READ_DB)}'):
    # 如果完全备份文件不存在就拷贝过来
    #    copy_ready()

    # unzip_backup()
    time = str(type('now', (), {'__repr__': lambda s: now_time()})())
    basename_folder = os.path.basename(READ_DB)  # 不包含文件夹路径，只取文件夹名字
    new_backup = r'.\backups\TimeBackup\{}\{}'.format(basename_folder, time)  # 生成以日期命名的文件夹
    if os.path.exists(new_backup) is False:
        os.makedirs(new_backup)

    read_full_db = Create_db(db_table, db_mode, db_data, original_file()[3])
    old_file_hash = [list_to_str(i) for i in read_full_db.search_sql('file_hash')]  # 原始完整备份的文件哈希值

    for root, dirs, filename in os.walk(TEMP_PATH):
        for file in filename:
            old_file_list.append(os.path.join(root, file))
        for dir_name in dirs:
            old_folder_list.append(os.path.join(root, dir_name))

    # 这里，因为需要与现在的文件夹里的内容做对比，但是因为将完全备份的文件解压到临时文件的原因，导致路径不同，会被视为两个不同的文件所以无法准确地对比
    # 因此，多做一步，将临时文件夹路径改成源文件的备份路径
    old_file = [file.replace(r'.\Temp', READ_DB) for file in old_file_list]
    old_folder = [folder.replace(r'.\Temp', READ_DB) for folder in old_folder_list]

    for root, dirs, filename in os.walk(READ_DB):
        for file in filename:
            new_file_list.append(os.path.join(root, file))
        for dir_name in dirs:
            new_folder_list.append(os.path.join(root, dir_name))

    for _old_file, _old_hash in zip(old_file_list, old_file_hash):
        old_dict[_old_file] = _old_hash

    for file in new_file_list:
        if file in old_file and Hash(file).md5() not in old_file_hash:
            # 判断文件是否备份修改，如果文件名相同，但哈希值不同可以判定为被修改
            add_backup.append(file)

        elif file not in old_file and Hash(file).md5() not in old_file_hash:
            # 如果文件不在备份文件里，而且哈希值也不在旧备份文件的哈希值里，可以判断是新增的文件
            # 记录一下问题，如果说原备份文件里存在空白文件，然后新增文件中也存在空白文件，就无法判定文件存在
            add_backup.append(file)

        elif file not in old_file and Hash(file).md5() in old_file_hash:
            # 如果文件不在备份文件里，但哈希值存在于旧备份文件，可以判定是被重命名
            add_backup.append(file)

    for folder in new_folder_list:
        if folder not in old_folder:
            # 如果文件夹不在备份文件夹，在新数据里，表示文件夹是新增文件夹
            add_backup.append(folder)

    backup_sys_temp = os.path.join(SYSTEM_TEMP, "OpenBackup")
    if not os.path.exists(backup_sys_temp):
        os.mkdir(backup_sys_temp)

    for data in add_backup:
        if os.path.isdir(data):
            shutil.copytree(data, os.path.join(backup_sys_temp, os.path.basename(data)))
        elif os.path.isfile(data):
            shutil.copy(data, os.path.join(backup_sys_temp, os.path.basename(data)))

    time_backup = fr'.\backups\TimeBackup\{os.path.basename(READ_DB)}'
    for archive_7z in os.listdir(time_backup)[0:-3]:
        archive.unzip(os.path.join(time_backup, archive_7z), backup_sys_temp)

    os.system(r'{} -mx5 -t7z a {} {}\* -mmt -sdel'.format('7z', '{}'.format(new_backup), backup_sys_temp))
    os.system(f'rd {new_backup}')
    showinfo('提示', '备份成功')


if __name__ == '__main__':
    differential_backup()
