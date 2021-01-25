from tkinter import Tk, Button
from tkinter.filedialog import askopenfilename

from Lib.safety.Signature import Signature
from config.Main_Config import LOGO


# --------------------------------数字验证----------------------------- #

def signature_box():
    def sign():
        s = Signature(askopenfilename(title='打开文件', filetypes=([('*', '.*')])))
        file_data = askopenfilename(title='打开私钥', filetypes=([('key', '.key')]))
        s.sign(file_data)
        win.quit()
        exit()

    win = Tk()  # 构造窗体

    _title = '数字签名'
    width = 250
    height = 90
    win.title(_title)
    win.iconbitmap(LOGO)

    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    aligner = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    win.geometry(aligner)

    Button(win, text='签名', command=sign).place(relx=0.1, rely=0.6, width=80, height=30)
    Button(win, text='验证').place(relx=0.56, rely=0.6, width=80, height=30)
    win.mainloop()

# signature_box()
