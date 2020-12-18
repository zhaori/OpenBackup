import os


def sys_move(old_folder, new_folder):
    # 移动文件
    os.system(r'move /y {} {} '.format(old_folder, new_folder))


def sys_copy(old_file, new_file):
    # 复制文件
    os.system(r'copy {} {}'.format(old_file, new_file))


def copy_folder(old_folder, new_folder):
    # 复制文件夹
    os.system(r'xcopy {} {} /S /H /E /Y'.format(old_folder, new_folder))


def del_file(folder):
    # 删除文件
    os.system("del {} /s /f /q".format(folder))
