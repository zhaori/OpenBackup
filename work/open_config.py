from tkinter import Tk, StringVar, Button
from tkinter.messagebox import showerror, showinfo
from tkinter.ttk import Combobox

from setting.MongoDB_Config import *
from setting.Main_Config import logo
from Lib.MongoDBSever import Mongodb_server


def get_db_table():
    return Mongodb_server(mongo_host, mongo_port).search_table('tasks')


class Open_tasks(object):
    def __init__(self):
        self.win = Tk()
        self.width = 250
        self.height = 200
        self.win.title('选择任务')

        self.win.iconbitmap(logo)
        screenwidth = self.win.winfo_screenwidth()
        screenheight = self.win.winfo_screenheight()
        aligner = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth - self.width) / 2,
                                   (screenheight - self.height) / 2)
        self.win.geometry(aligner)
        self.db = Mongodb_server(mongo_host, mongo_port)

    def handle(self, *args):
        name = self.db.search_one(f"tasks", self.comboxlist.get(), {"_id": 0, 'folder': 1})
        data = {
            "task": name['folder'],
            "state": 1
        }
        return data

    def _exit_win(self):
        self.win.quit()

    def ok(self):
        # 先清空表再插入数据
        try:
            self.db.del_table('select')
        except:
            pass
        finally:
            self.db.insert('select', self.comboxlist.get(), self.handle())
            showinfo('提示', '任务已选择')
            self._exit_win()

    def _win(self):
        comvalue = StringVar()  # 窗体自带的文本，新建一个值
        self.comboxlist = Combobox(self.win, textvariable=comvalue, state='readonly')  # 初始化
        self.comboxlist["values"] = tuple(get_db_table())
        try:
            self.comboxlist.current(0)  # 选择第一个
        except:
            showerror('运行错误', '差异备份的备份文件不存在')
            exit()

        self.comboxlist.bind("<<ComboboxSelected>>", self.handle)  # 绑定事件,(下拉列表框被选中时，绑定handle()函数)
        self.comboxlist.place(relx=0.2, rely=0.25, width=140, height=35)

    def Main(self):
        self._win()
        Button(self.win, text='确定', command=self.ok).place(relx=0.05, rely=0.75, width=70, height=30)
        Button(self.win, text='取消', command=self._exit_win).place(relx=0.68, rely=0.75, width=70, height=30)
        self.win.mainloop()


def open_tasks():
    # 加载配置文件
    Open_tasks().Main()


# open_config()
if __name__ == '__main__':
    open_tasks()

