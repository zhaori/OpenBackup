import os
from tkinter import Tk, StringVar, Label, Button
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox

from Lib.safety.hash import Hash
from config.db_config import tk_title, logo, windll




class TimeBackup(object):
    def __init__(self):
        self.win = Tk()
        self.width = 250
        self.height = 200
        self.win.title(tk_title)
        # self.win.iconbitmap(logo)
        windll.shell32.SetCurrentProcessExplicitAppUserModelID('version')  # 任务栏图标

        screenwidth = self.win.winfo_screenwidth()
        screenheight = self.win.winfo_screenheight()
        aligner = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.win.geometry(aligner)

    def handle(self, *args):
        pass

    def exit_os(self):
        # 退出
        self.win.quit()
        exit()

    def window(self):
        comvalue = StringVar()  # 窗体自带的文本，新建一个值S
        comboxlist = Combobox(self.win, textvariable=comvalue, state='readonly')  # 初始化

        comboxlist["values"] = ('选择日期', "MD5", "SHA1", "SHA256")
        comboxlist.current(0)  # 选择第一个
        comboxlist.bind("<<ComboboxSelected>>", self.handle)  # 绑定事件,(下拉列表框被选中时，绑定handle()函数)
        comboxlist.place(relx=0.1, rely=0.4, width=200, height=35)
        Label(self.win, text='时间机器', font=("微软雅黑", 16)).place(relx=0.11, rely=0.12, width=200, height=30)
        Button(self.win, text='确定', command=self.exit_os).place(relx=0.12, rely=0.75, width=80, height=30)
        Button(self.win, text='取消', command=self.exit_os).place(relx=0.56, rely=0.75, width=80, height=30)
        self.win.mainloop()




if __name__ == '__main__':
    TimeBackup().window()
