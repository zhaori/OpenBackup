import os


def sys_move(old_folder, new_folder):
    os.system(r'move /y {} {} '.format(old_folder, new_folder))


def sys_copy(old_file, new_file):
    os.system(r'copy {} {}'.format(old_file, new_file))


def copy_folder(old_folder, new_folder):
    os.system(r'xcopy /self /e {} {}'.format(old_folder, new_folder))
