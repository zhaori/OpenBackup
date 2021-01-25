import os
from tkinter import Tk, Button, Label
from tkinter.filedialog import askopenfilename

from Lib.safety.Hash import Hash, verify
from config.Main_Config import LOGO


def tool_hash():
    def sign():
        def return_hash(h_hash):
            if h_hash == '.md5':
                return Hash(askopenfilename(title='打开文件', filetypes=([('*', '.*')]))).md5()
            elif h_hash == '.sha1':
                return Hash(askopenfilename(title='打开文件', filetypes=([('*', '.*')]))).sha1()
            elif h_hash == '.sha256':
                return Hash(askopenfilename(title='打开文件', filetypes=([('*', '.*')]))).sha256()
            else:
                pass

        file_data = askopenfilename(title='打开哈希文件',
                                    filetypes=([('md5', '.md5'), ('sha1', '.sha1'), ('sha256', '.sha256')]))
        hash_suffix = os.path.splitext(file_data)[1]

        with open(file_data, 'r') as f:
            h = f.read()

        if verify(return_hash(hash_suffix), h) is False:
            Label(text='验证失败', font=('宋体', '13')).place(relx=0.32, rely=0.1, width=80, height=30)
        elif verify(return_hash(hash_suffix), h) is True:
            Label(text='验证通过', font=('宋体', '13')).place(relx=0.32, rely=0.1, width=80, height=30)

    win = Tk()  # 构造窗体

    _title = '哈希验证'
    width = 250
    height = 90
    win.title(_title)
    win.iconbitmap(LOGO)

    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    aligner = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    win.geometry(aligner)
    Button(win, text='选择', command=sign).place(relx=0.32, rely=0.6, width=80, height=30)
    win.mainloop()


if __name__ == '__main__':
    tool_hash()
