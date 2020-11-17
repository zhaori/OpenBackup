import os
from tkinter import Tk, StringVar, Button
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from Lib.Pydos import copy_folder
from tkinter.ttk import Combobox
from Lib.Number_CN import cn_num, num_cn
from Lib.sqlite import Create_db, list_to_str
from config.db_config import logo, windll
from config.Differential_config import df_db_mode, df_db_data
from Lib.z7 import archive

# 返回数据库绝对路径
DB = r'D:\OneDrive\Python\exploitation\OpenBackup\backups\TimeBackup\文件资源管理器.db'


class recovery(object):
    """
    时间机器
    """

    def __init__(self):
        self.db = Create_db(path=DB)

    def get_table(self):
        """
        获取所有的表
        """
        table_list = []
        for table in self.db.search_table():
            table_list.append(list_to_str(table))
        return table_list

    def search(self):
        pass


class window(object):
    def __init__(self):
        self.win = Tk()
        self.width = 250
        self.height = 200
        self.win.title('TimeBackup')
        # self.data = None
        # self.win.iconbitmap(logo)
        windll.shell32.SetCurrentProcessExplicitAppUserModelID('version')
        screenwidth = self.win.winfo_screenwidth()
        screenheight = self.win.winfo_screenheight()
        aligner = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth - self.width) / 2,
                                   (screenheight - self.height) / 2)
        self.win.geometry(aligner)

    def _exit_win(self):
        self.win.quit()
        exit()

    def handle(self, *args):
        t = self.comboxlist.get()
        d = "{}{}{}{}{}".format(t[0:4], t[5:7], t[8:10], t[11:13], t[14:16])
        return d

    def ok(self):
        """
        确定按钮
        """
        old_file = []
        db = Create_db(num_cn(self.handle()), df_db_mode, df_db_data, path=DB)
        reduce_file = list_to_str(db.search_sql('reduce')[0])
        unzip = archive(reduce_file, './Temp')
        unzip.unzip(reduce_file, './Temp')

        for file in db.search_sql('difference'):
            if num_cn(self.handle()) in recovery().get_table():
                old_file.append(list_to_str(file))

        for i in os.listdir('./Temp'):
            for file in old_file:
                copy_folder(os.path.abspath(i), file)

        self.win.quit()

    def _win(self):
        comvalue = StringVar()  # 窗体自带的文本，新建一个值
        self.comboxlist = Combobox(self.win, textvariable=comvalue, state='readonly')  # 初始化
        self.table_time = []
        for time in recovery().get_table():
            ge_shi = cn_num(time)

            self.table_time.append("{}-{}-{} {}:{}".format(ge_shi[0:4], ge_shi[5:7],
                                                           ge_shi[6:8], ge_shi[8:10], ge_shi[10:12]))
            """
            self.data = {
                "year": ge_shi[0:4],
                "month": ge_shi[5:7],
                "day": ge_shi[6:8],
                "hour": ge_shi[8:10],
                "minute": ge_shi[10:12]
            }
            """
        self.comboxlist["values"] = tuple(self.table_time)
        self.comboxlist.current(0)  # 选择第一个
        self.comboxlist.bind("<<ComboboxSelected>>", self.handle)  # 绑定事件,(下拉列表框被选中时，绑定handle()函数)
        self.comboxlist.place(relx=0.2, rely=0.25, width=140, height=35)

    def Main(self):
        self._win()
        Button(self.win, text='确定', command=self.ok).place(relx=0.05, rely=0.75, width=70, height=30)
        Button(self.win, text='取消', command=self._exit_win).place(relx=0.68, rely=0.75, width=70, height=30)
        self.win.mainloop()


def recover():
    window().Main()



if __name__ == '__main__':
    recover()
