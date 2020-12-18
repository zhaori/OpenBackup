# 还原备份
"""
还原文件，解压后会得到一个多余、重复的文件夹，比如 压缩D:/123文件夹，那么生成的压缩文件夹结构为：123/123
因此，处理的办法是直接将文件夹解压到Temp临时文件夹后移动到目的文件夹
但shutil模块会引起PermissionError错误即权限不足问题，因此这里直接调用的是Windows系统DOS命令进行移动
如后续需要支持跨平台，可以加一句系统判断后利用系统原生命令进行处理
"""
import os
from setting.Main_Config import READ_DB
from tkinter.messagebox import showinfo

from Lib.PyDOS import sys_move
from Lib.z7 import archive

from setting.DB_Config import data_path


def full_reduction():
    # 还原备份

    system_temp = r'.\Temp'  # 指定一个临时文件夹
    if os.path.exists(system_temp) is False:
        os.mkdir(system_temp)

    # os.path.basename截取全路径最后一个反斜杠，可以是文件夹或文件
    folder_file = os.path.basename(READ_DB)  # 获取文件夹名，不包含路径
    folder_above = os.path.dirname(READ_DB)  # 获取路径最后一个反斜杠前的内容，在这里意为获取目录的上一级
    new_zip = archive(data_path, READ_DB)
    file_7z = '{}/{}.7z'.format(data_path, folder_file)
    new_zip.unzip(file_7z, system_temp)

    folder_temp = r'{}\{}'.format(system_temp, folder_file)
    # if os.path.exists(folder) is True:
    #    windows_show('文件夹已存在,是否删除目标文件夹还原？')
    if os.path.exists(READ_DB) is False:
        # os.system(r'move /y {} {} '.format(folder_temp, folder_above))
        sys_move(folder_temp, folder_above)
        showinfo(title='提示', message='处理完毕')


if __name__ == "__main__":
    # full_reduction()
    pass
