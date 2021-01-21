import os
from tkinter import Tk, StringVar, Label, Button
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox

from Lib.safety.Hash import Hash
from config.Main_Config import tk_title, logo


# ----------------------生成哈希值----------------- #
def hash_box():
    win = Tk()  # 构造窗体

    def exit_os():
        # 退出
        win.quit()
        exit()

    def handle(*args):  # 处理事件，*args表示可变参数

        filename = str(askopenfilename())
        hash_path, hash_file = os.path.split(filename)
        h = Hash(filename)
        if comboxlist.get() == "MD5":
            h.sava_hash(h.md5(), '.md5', hash_path)

        elif comboxlist.get() == "SHA1":
            h.sava_hash(h.sha1(), '.sha1', hash_path)

        elif comboxlist.get() == "SHA256":
            h.sava_hash(h.sha256(), '.sha256', hash_path)

    width = 250
    height = 200
    win.title(tk_title)
    win.iconbitmap(logo)

    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    aligner = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    win.geometry(aligner)

    comvalue = StringVar()  # 窗体自带的文本，新建一个值S
    comboxlist = Combobox(win, textvariable=comvalue, state='readonly')  # 初始化
    comboxlist["values"] = ('选择方法', "MD5", "SHA1", "SHA256")
    comboxlist.current(0)  # 选择第一个
    comboxlist.bind("<<ComboboxSelected>>", handle)  # 绑定事件,(下拉列表框被选中时，绑定handle()函数)
    comboxlist.place(relx=0.1, rely=0.4, width=200, height=35)
    Label(win, text='计算哈希', font=("微软雅黑", 16)).place(relx=0.11, rely=0.12, width=200, height=30)
    Button(win, text='确定', command=exit_os).place(relx=0.12, rely=0.75, width=80, height=30)
    Button(win, text='取消', command=exit_os).place(relx=0.56, rely=0.75, width=80, height=30)
    win.mainloop()


if __name__ == '__main__':
    hash_box()
