# 完全备份
"""
还原文件，解压后会得到一个多余、重复的文件夹，比如 压缩D:/123文件夹，那么生成的压缩文件夹结构为：123/123
因此，处理的办法是直接将文件夹解压到C:/WINDOWS/Temp临时文件夹后移动到目的文件夹
但shutil模块会引起PermissionError错误即权限不足问题，因此这里直接调用的是Windows系统DOS命令进行移动
如后续需要支持跨平台，可以加一句系统判断后利用系统原生命令进行处理
"""
import os
from tkinter import Tk, Button, Label
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

from Lib.Pydos import sys_move
from Lib.json_py import PyJson
from Lib.z7 import archive
from config.db_config import data_path
from config.db_config import windll


def full_reduction():
    # 还原备份
    def windows_show(text):
        win = Tk()  # 构造窗体
        windll.shell32.SetCurrentProcessExplicitAppUserModelID('version')  # 任务栏图标

        _title = '还原提示'
        width = 250
        height = 90
        win.title(_title)
        # win.iconbitmap(logo)

        screenwidth = win.winfo_screenwidth()
        screenheight = win.winfo_screenheight()
        aligner = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        win.geometry(aligner)

        def return_ok():
            # str(folder).replace('/', '\\')
            os.system('rmdir /s/q {}'.format(folder))
            os.system(r'move /y {} {} '.format(folder_temp, folder_above))
            win.quit()
            exit()

        def return_no():
            win.quit()
            exit()

        Label(win, text=text, font=('宋体', '9')).place(relx=0.08, rely=0.2)
        Button(win, text='确定', command=return_ok).place(relx=0.1, rely=0.6, width=80, height=30)
        Button(win, text='取消', command=return_no).place(relx=0.56, rely=0.6, width=80, height=30)
        win.mainloop()

    system_temp = r'.\Temp'  # 指定一个临时文件夹
    if os.path.exists(system_temp) is False:
        os.mkdir(system_temp)
    open_file = askopenfilename(title='打开任务文件', filetypes=([('json', '.json')]))
    p_j = PyJson(open_file)
    folder = p_j.read('folder')  # 全路径
    # os.path.basename截取全路径最后一个反斜杠，可以是文件夹或文件
    folder_file = os.path.basename(folder)  # 获取文件夹名，不包含路径
    folder_above = os.path.dirname(folder)  # 获取路径最后一个反斜杠前的内容，在这里意为获取目录的上一级
    new_zip = archive(data_path, folder)
    file_7z = '{}/{}.7z'.format(data_path, folder_file)
    new_zip.unzip(file_7z, system_temp)

    folder_temp = r'{}\{}'.format(system_temp, folder_file)
    if os.path.exists(folder) is True:
        windows_show('文件夹已存在,是否删除目标文件夹还原？')

    elif os.path.exists(folder) is False:
        # os.system(r'move /y {} {} '.format(folder_temp, folder_above))
        sys_move(folder_temp, folder_above)
        showinfo(title='提示', message='处理完毕')


if __name__ == "__main__":
    # full_reduction()
    pass
