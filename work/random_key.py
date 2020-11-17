from tkinter import Tk, IntVar, Radiobutton, Label, StringVar, Entry

from Lib.safety.Hash import Create_AESKey
from config.db_config import *


def random_key():
    root = Tk()
    width = 350
    height = 250
    root.title('随机密钥')
    root.iconbitmap(logo)
    # root.resizable(False, False)
    # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    aligner = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(aligner)
    v = IntVar()
    e = StringVar()

    def get_value():
        e.set(Create_AESKey(v.get()))

    r1 = Radiobutton(root, text="16 bit", value=16, variable=v, command=get_value)
    r1.place(relx=0.1, rely=0.68, width=60, height=10)

    r2 = Radiobutton(root, text="32 bit", value=32, variable=v, command=get_value)
    r2.place(relx=0.4, rely=0.68, width=60, height=10)

    r3 = Radiobutton(root, text="64 bit", value=64, variable=v, command=get_value)
    r3.place(relx=0.7, rely=0.68, width=60, height=10)

    r4 = Radiobutton(root, text="128 bit", value=128, variable=v, command=get_value)
    r4.place(relx=0.109, rely=0.79, width=60, height=10)

    r5 = Radiobutton(root, text="256 bit", value=256, variable=v, command=get_value)
    r5.place(relx=0.409, rely=0.79, width=60, height=10)

    r6 = Radiobutton(root, text="512 bit", value=512, variable=v, command=get_value)
    r6.place(relx=0.709, rely=0.79, width=60, height=10)

    Label(root, text='Ctrl+A全选复制', font=("微软雅黑", 12)).place(relx=0.15, rely=0.06, width=260, height=30)

    wb = Entry(root, textvariable=e, width=200)
    wb.place(rely=0.38, width=350, height=30)

    root.mainloop()


if __name__ == "__main__":
    random_key()
