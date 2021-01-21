import os
from ctypes import windll
from tkinter import Tk, StringVar, Button
from tkinter.messagebox import showerror
from tkinter.ttk import Combobox

from Lib.z7 import archive
from config.Main_Config import READ_DB, logo

BACKUP_FILE: str


def get_file():
    """
    获取所有的差异备份文件
    """
    global BACKUP_FILE
    basename_folder = os.path.basename(READ_DB)  # 不包含文件夹路径，只取文件夹名字
    BACKUP_FILE = r'.\backups\TimeBackup\{}'.format(basename_folder)
    return os.listdir(BACKUP_FILE)


class recovery_win(object):
    def __init__(self):
        self.win = Tk()
        self.width = 250
        self.height = 200
        self.win.title('TimeBackup')

        self.win.iconbitmap(logo)
        windll.shell32.SetCurrentProcessExplicitAppUserModelID('version')
        screenwidth = self.win.winfo_screenwidth()
        screenheight = self.win.winfo_screenheight()
        aligner = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth - self.width) / 2,
                                   (screenheight - self.height) / 2)
        self.win.geometry(aligner)
        # self.recovery_folder = READ_DB

    def _exit_win(self):
        self.win.quit()
        exit()

    def handle(self, *args):
        # 获取列表下拉选项
        t = self.comboxlist.get()
        d = f"{t[0:4]}{t[5:7]}{t[8:10]}{t[11:13]}{t[14:16]}"
        return t, d

    def ok(self):

        for root, dirs, file in os.walk(READ_DB):
            [os.remove(os.path.join(root, f)) for f in file if root and file]  # 清空源文件夹的内容

        t, d = recovery_win.handle(self)
        differ_archive = os.path.join(BACKUP_FILE, f"{d}{'.7z'}").replace('/', '\\')
        unzip = archive(differ_archive, READ_DB)
        unzip.unzip(differ_archive, READ_DB)

    def _win(self):
        comvalue = StringVar()  # 窗体自带的文本，新建一个值
        self.comboxlist = Combobox(self.win, textvariable=comvalue, state='readonly')  # 初始化
        self.table_time = []

        for get_time in get_file():
            self.table_time.append(
                f"{get_time[0:4]}-{get_time[4:6]}-{get_time[6:8]} {get_time[8:10]}:{get_time[10:12]}")

        self.comboxlist["values"] = tuple(self.table_time)
        try:
            self.comboxlist.current(0)  # 选择第一个
        except:
            showerror('运行错误', '差异备份的备份文件不存在')
            exit()

        self.comboxlist.bind("<<ComboboxSelected>>", self.handle)  # 绑定事件,(下拉列表框被选中时，绑定handle()函数)
        self.comboxlist.place(relx=0.2, rely=0.25, width=140, height=35)

    # noinspection PyPep8Naming
    def main(self):
        self._win()
        Button(self.win, text='确定', command=self.ok).place(relx=0.05, rely=0.75, width=70, height=30)
        Button(self.win, text='取消', command=self._exit_win).place(relx=0.68, rely=0.75, width=70, height=30)
        self.win.mainloop()


def recovery_run():
    recovery_win().main()


if __name__ == '__main__':
    recovery_run()
