import os
from tkinter import Tk, StringVar, Label, Button
from tkinter.ttk import Combobox

from Lib.time_json import create_json
from setting.Main_Config import logo


class drop_menu(object):
    """
    下拉框自动生成
    """

    def __init__(self, root):
        self._root = root
        self._width = 60
        self._height = 30

    def handle(self, *args):  # 处理事件
        with open('begin_time', 'a+', encoding='utf-8') as f:
            f.write(self.comboxlist.get())
        with open('begin_time', 'r', encoding='utf-8') as f:
            str_time = f.read()

        create_json('begin', str_time)

    def new(self, x, y, begin, end):
        """
        x,y是定位
        begin,end是列表元素范围
        add是绑定
        """
        comvalue = StringVar()
        self.comboxlist = Combobox(self._root, textvariable=comvalue, state='readonly')  # 初始化
        v_list = []
        for n in range(begin, end):
            if n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:  # 使用24小时
                v_list.append('{}{}'.format(0, n))
            else:
                v_list.append(n)
        self.comboxlist["values"] = tuple(v_list)
        self.comboxlist.current(0)  # 选择第一个元素
        self.comboxlist.bind("<<ComboboxSelected>>", self.handle)  # 绑定事件,(下拉列表框被选中时，绑定handle()函数)
        self.comboxlist.place(relx=x, rely=y, width=self._width, height=self._height)

    @staticmethod
    def clean():
        # time_file = ['begin_time.txt', 'end_time.txt']
        if os.path.isfile('begin_time') is True:
            os.remove('begin_time')


class calendar(object):
    def __init__(self):
        self._width = 350
        self._height = 200
        self._win = Tk()
        self._win.title('开始时间')
        self._win.iconbitmap(logo)

        # 居中
        screenwidth = self._win.winfo_screenwidth()
        screenheight = self._win.winfo_screenheight()
        aligner = '%dx%d+%d+%d' % (
            self._width, self._height, (screenwidth - self._width) / 2, (screenheight - self._height) / 2)
        self._win.geometry(aligner)

    def _exit(self):
        self._win.quit()
        exit()

    def _get_value(self):
        self._win.quit()
        exit()

    def list_value(self):
        # 下拉框布局
        # menu = drop_menu(self._win)
        drop_menu(self._win).new(0.1, 0.1, 2020, 2099)  # 年
        drop_menu(self._win).new(0.4, 0.1, 1, 13)  # 月
        drop_menu(self._win).new(0.7, 0.1, 1, 32)  # 日
        drop_menu(self._win).new(0.1, 0.3, 1, 25)  # 时
        drop_menu(self._win).new(0.4, 0.3, 0, 60)  # 分
        # drop_menu(self._win).new(0.7, 0.3, 1, 60)  # 秒

    def window(self):
        # 文字按钮布局
        Label(text='年').place(relx=0.28, rely=0.1, width=30, height=30)
        Label(text='月').place(relx=0.58, rely=0.1, width=30, height=30)
        Label(text='日').place(relx=0.88, rely=0.1, width=30, height=30)
        Label(text='时').place(relx=0.28, rely=0.3, width=30, height=30)
        Label(text='分').place(relx=0.58, rely=0.3, width=30, height=30)
        # Label(text='秒').place(relx=0.88, rely=0.3, width=30, height=30)
        Button(self._win, text='确定', command=self._get_value).place(relx=0.12, rely=0.75, width=80, height=30)
        Button(self._win, text='取消', command=self._exit).place(relx=0.56, rely=0.75, width=80, height=30)
        self._win.mainloop()


def begin_time():
    c = calendar()
    c.list_value()
    c.window()
    exit()


if __name__ == '__main__':
    begin_time()
