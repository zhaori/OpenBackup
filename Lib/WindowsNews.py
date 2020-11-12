import os
from tkinter import messagebox, Tk, Frame


def show_error(message):
    """
    return: message:传入错误具体信息
    """
    root = Tk()
    width = 380
    height = 300
    root.title('Debug Error')
    # Label(root, text='错误已记入log日志文件', font=("微软雅黑", 16)).pack()
    # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    aligner = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(aligner)
    frame = Frame(root)
    frame.pack()
    messagebox.showerror(title='Python Script Error', message=message)
    os._exit(0)
    # root.mainloop()
    # return message


if __name__ == "__main__":
    t = "202009241746   C:/Users/zgz/Documents/Pycharm-workspace/exploitation/long distance notes/Lib/collect.py      " \
        "21     <class Lib.Error.Data_Type_Error> "
    show_error(t)
