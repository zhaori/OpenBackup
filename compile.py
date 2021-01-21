import os
from threading import Thread

"""
:compile_list 编译文件的路径
"""

compile_list = [
    "listen_service.pyw",
    r".\work\begin_calendar.pyw",
    r".\work\end_calendar.pyw",
    "watch_listen.pyw",
    "AddPATH.py",
    "Main.pyw"
]


def get_compile(file, icon):
    os.system(f"pyinstaller -F {file} -i {icon} --noconsole")


thread_list = [Thread(target=get_compile, args=(i, r'main.ico')) for i in compile_list]
for i in thread_list:
    i.start()
for i in thread_list:
    i.join()
