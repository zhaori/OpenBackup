import json
import os
from tkinter import Tk, Label, Entry, Button
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo

from Lib.json_py import PyJson
from config.db_config import tk_title, logo
from Lib.time_json import file_json


# ---------------------创建计划任务--------------- #
class New_Task(object):
    def __init__(self):
        self.root = Tk()
        self.width = 320
        self.height = 200
        self.root.title(tk_title)
        self.root.iconbitmap(logo)
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        aligner = '%dx%d+%d+%d' % (
            self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.root.geometry(aligner)
        self.entry = None

    @staticmethod
    def _task():
        os.system(r'python work\begin_calendar.py')
        os.system(r'python work\end_calendar.py')

        data = {
            'begin': file_json().read_time('begin'),
            'end': file_json().read_time('end'),
            'folder': str(askdirectory())
        }

        data_json = eval(str(json.dumps(data)))
        p = PyJson('./json_file.json')
        p.write(data_json)
        showinfo('Super Backups', '任务生成成功')
        time_file = ['begin_time', 'end_time', 'time.json']
        for file in time_file:
            if os.path.isfile(file):
                os.remove(file)

    def _old_new(self):
        try:
            os.rename('./json_file.json', self.entry.get())  # 重命名
            os.remove('./json_file.json')  # 删除
            self.root.quit()
            exit()
        except FileNotFoundError:
            pass

    def window(self):
        self.entry = Entry(self.root, bd=2)  # 重命名
        self.entry.place(relx=0.7, rely=0.28, width=80, height=30)
        Button(self.root, text='生成任务', command=self._task).place(relx=0.16, rely=0.6, width=90, height=40)
        Label(self.root, text='新任务', font=("微软雅黑", 16)).place(relx=0.19, width=200, height=30)
        Label(self.root, text='任务名：', font=("微软雅黑", 10)).place(relx=0.48, rely=0.28, width=70, height=30)
        Button(self.root, text='重命名', command=self._old_new).place(relx=0.68, rely=0.6, width=90, height=40)
        self.root.mainloop()


def new_task():
    New_Task().window()


if __name__ == '__main__':
    new_task()
