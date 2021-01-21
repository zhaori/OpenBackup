import os
from threading import Thread

"""
:compile_list 编译文件的路径，可以为绝对路径或相对路径，在路径前加r，以python解释器分辨为字符串
"""

compile_list = [
    "listen_service.pyw"
]


def get_compile(file, icon):
    os.system(f"pyinstaller -F {file} -i {icon} --noconsole")


thread_list = [Thread(target=get_compile, args=(i, r'main.ico')) for i in compile_list]
for i in thread_list:
    i.start()
for i in thread_list:
    i.join()
