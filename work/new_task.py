import json
import os
from tkinter import Tk, Label, Entry, Button
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo

from Lib.json_py import PyJson
from config.db_config import tk_title, logo


# ---------------------创建计划任务--------------- #
def new_task():
    root = Tk()
    width = 450
    height = 360
    root.title(tk_title)
    root.iconbitmap(logo)
    # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    aligner = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(aligner)
    Label(root, text='新计划任务', font=("微软雅黑", 16)).place(relx=0.3, width=200, height=30)
    Label(root, text='开始时间', font=("微软雅黑", 10)).place(relx=0.11, rely=0.12, width=50, height=30)
    Label(root, text='结束时间', font=("微软雅黑", 10)).place(relx=0.55, rely=0.12, width=52, height=30)
    Label(root, text='具体几时', font=("微软雅黑", 10)).place(relx=0.09, rely=0.28, width=70, height=30)
    Label(root, text='任务名：', font=("微软雅黑", 10)).place(relx=0.53, rely=0.28, width=70, height=30)

    # 输入框设置
    entry = Entry(root, bd=2)
    entry.place(relx=0.26, rely=0.12, width=80, height=30)
    entry2 = Entry(root, bd=2)
    entry2.place(relx=0.7, rely=0.12, width=80, height=30)
    entry3 = Entry(root, bd=2)
    entry3.place(relx=0.26, rely=0.28, width=80, height=30)
    entry4 = Entry(root, bd=2)
    entry4.place(relx=0.7, rely=0.28, width=80, height=30)

    # 设定年月日格式 XXXXXXXX
    def task():
        data = {
            'begin': entry.get() + entry3.get(),
            'end': entry2.get() + entry3.get(),
            'folder': str(askdirectory())
        }

        data_json = eval(str(json.dumps(data)))
        p = PyJson('./json_file.json')
        p.write(data_json)
        showinfo('Super Backups', '任务生成成功')

    Button(root, text='立即生成任务', command=task).place(relx=0.18, rely=0.46, width=90, height=40)

    def old_new():  # 任务重命名
        try:
            os.rename('./json_file.json', entry4.get())  # 重命名
            os.remove('./json_file.json')  # 删除
            os._exit(0)
        except FileNotFoundError:
            pass

    Button(root, text='任务重命名', command=old_new).place(relx=0.62, rely=0.46, width=90,
                                                      height=40)
    root.mainloop()


new_task()
