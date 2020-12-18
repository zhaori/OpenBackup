from tkinter import Tk, IntVar, Radiobutton, Entry, StringVar, Label
from Lib.safety.Hash import Create_AESKey
from tkinter.ttk import Combobox
from setting.Main_Config import windll, logo
from threading import Thread


class create_key(object):
    def __init__(self):
        self.root = Tk()
        self.width = 350
        self.height = 250
        self.root.title('随机密钥')
        self.root.iconbitmap(logo)
        # root.resizable(False, False)
        windll.shell32.SetCurrentProcessExplicitAppUserModelID('version')  # 任务栏图标
        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        aligner = '%dx%d+%d+%d' % (
            self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.root.geometry(aligner)
        self.v = IntVar()
        self.e = StringVar()
        self.comvalue = StringVar()  # 窗体自带的文本，新建一个值S
        self.comboxlist = Combobox(self.root, textvariable=self.comvalue, state='readonly')  # 初始化

    def _exit(self):
        self.root.quit()

    def get_value(self):
        """
        :return: 获取key
        """
        self.e.set(Create_AESKey(self.v.get()))

    def _win(self):
        r1 = Radiobutton(self.root, text="16 bit", value=16, variable=self.v, command=self.get_value)
        r1.place(relx=0.1, rely=0.68, width=60, height=10)

        r2 = Radiobutton(self.root, text="32 bit", value=32, variable=self.v, command=self.get_value)
        r2.place(relx=0.4, rely=0.68, width=60, height=10)

        r3 = Radiobutton(self.root, text="64 bit", value=64, variable=self.v, command=self.get_value)
        r3.place(relx=0.7, rely=0.68, width=60, height=10)

        r4 = Radiobutton(self.root, text="128 bit", value=128, variable=self.v, command=self.get_value)
        r4.place(relx=0.109, rely=0.79, width=60, height=10)

        r5 = Radiobutton(self.root, text="256 bit", value=256, variable=self.v, command=self.get_value)
        r5.place(relx=0.409, rely=0.79, width=60, height=10)

        r6 = Radiobutton(self.root, text="512 bit", value=512, variable=self.v, command=self.get_value)
        r6.place(relx=0.709, rely=0.79, width=60, height=10)

    def run(self):
        self._win()
        Label(self.root, text='Ctrl+A全选复制', font=("微软雅黑", 12)).place(relx=0.15, rely=0.06, width=260, height=30)
        wb = Entry(self.root, textvariable=self.e, width=200)
        wb.place(rely=0.38, width=350, height=30)

        self.root.mainloop()


def _run():
    create_key().run()


def key():
    Thread(target=_run).start()


if __name__ == "__main__":
    key()
