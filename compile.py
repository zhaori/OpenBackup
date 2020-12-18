import os
from threading import Thread


"""
:compile_list 编译文件的路径，可以为绝对路径或相对路径，在路径前加r，以python解释器分辨为字符串
"""
"""
    r"D:\OneDrive\Python\exploitation\OpenBackup\source\listen_service.pyw",
    r"D:\OneDrive\Python\exploitation\OpenBackup\source\Main.pyw",
     r"D:\OneDrive\Python\exploitation\OpenBackup\source\random_key.pyw",
    r"D:\OneDrive\Python\exploitation\OpenBackup\source\watch_listen.pyw"
"""
compile_list = [

]


def get_compile(file, icon):
    os.system("pyinstaller -F {} -i {}".format(file, icon))


thead_list = [Thread(target=get_compile, args=(i, './应用.ico')) for i in compile_list]
for i in thead_list:
    i.start()
for i in thead_list:
    i.join()

# 做一点清理工作
for spec, build_info in zip(os.listdir('/'), os.listdir('临时归档/build')):
    file, suffix = os.path.splitext(spec)
    if suffix == '.spec':
        os.remove(spec)
    if os.path.isfile(build_info):
        os.remove(build_info)
    elif os.path.isdir(build_info):
        os.rmdir(build_info)