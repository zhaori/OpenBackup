from tkinter import Tk, StringVar, Button
from tkinter.messagebox import showerror
from tkinter.ttk import Combobox

from Lib.MongoDBSever import Mongodb_server
from config.Main_Config import LOGO
from config.MongoDB_Config import mongo_host, mongo_port


def get_db_table():
    return Mongodb_server(mongo_host, mongo_port).search_table('tasks')


class delete_tasks(object):
    def __init__(self):
        self.win = Tk()
        self.width = 250
        self.height = 200
        self.win.title('选择任务')

        self.win.iconbitmap(LOGO)
        screenwidth = self.win.winfo_screenwidth()
        screenheight = self.win.winfo_screenheight()
        aligner = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth - self.width) / 2,
                                   (screenheight - self.height) / 2)
        self.win.geometry(aligner)
        self.db = Mongodb_server(mongo_host, mongo_port)

    def handle(self, *args):
        name = self.db.search_one(f"tasks", self.comboxlist.get(), {"_id": 0, 'begin': 1, 'end': 1, 'folder': 1})
        data = {
            "folder": name['folder']
        }
        return data

    def _exit_win(self):
        self.win.quit()

    def ok(self):
        self.db.del_key('tasks', self.comboxlist.get(), self.handle())
        self._win()

    def _win(self):
        comvalue = StringVar()  # 窗体自带的文本，新建一个值
        self.comboxlist = Combobox(self.win, textvariable=comvalue, state='readonly')  # 初始化
        self.comboxlist["values"] = tuple(get_db_table())
        try:
            self.comboxlist.current(0)  # 选择第一个
        except:
            showerror('运行错误', '没有任务')
            self.win.quit()

        self.comboxlist.bind("<<ComboboxSelected>>", self.handle)  # 绑定事件,(下拉列表框被选中时，绑定handle()函数)
        self.comboxlist.place(relx=0.2, rely=0.25, width=140, height=35)

    # noinspection PyPep8Naming
    def main(self):
        self._win()
        Button(self.win, text='删除', command=self.ok).place(relx=0.05, rely=0.75, width=70, height=30)
        Button(self.win, text='取消', command=self._exit_win).place(relx=0.68, rely=0.75, width=70, height=30)
        self.win.mainloop()


def task_delete():
    delete_tasks().main()


if __name__ == '__main__':
    task_delete()
