import os
from tkinter import Menu, Tk, Text, END, INSERT
from tkinter.messagebox import showinfo
from config.db_config import *
from work import *

os.system('path=%path%;./')


def about_main():
    showinfo(tk_title, '        本程序遵守GPL 3.0协议开源\n '
                       '                 @ Python3.7  \n '
                       ' https://github.com/zhaori/OpenBackup')


def t_help():
    os.system(r'help.txt')


def random_key():
    os.system(r'python work\random_key.py')


def main():
    def _quit():
        root.quit()
        root.destroy()
        exit()

    root = Tk()
    root.iconbitmap(logo)

    width = 518
    height = 360
    root.title(tk_title)

    text = Text(root)
    text.grid(row=2, column=2, columnspan=6, rowspan=15)

    # 获取数据
    data = open('./doc/LICENSE', encoding='utf-8').read()
    # 填充到text控件
    text.delete(1.0, END)
    text.insert(INSERT, data)

    menbar = Menu(root)  # 界面
    fmenu = Menu(menbar)  # 文件
    fmenu.add_command(label='新建任务', command=new_task)
    fmenu.add_command(label='修改任务', command=open_take)
    fmenu.add_command(label='修改配置', command=open_config)
    fmenu.add_separator()
    fmenu.add_command(label='退出', command=_quit)
    menbar.add_cascade(label='文件', menu=fmenu)  # 绑定到一级菜单

    hymenu = Menu(menbar)
    bf_menu = Menu(root)  # 新建二级菜单绑定子选项
    huanyuan = Menu(root)
    bf_menu.add_command(label='完全备份', command=full_backup)
    bf_menu.add_command(label='差异备份', command=differ_backup)
    # bf_menu.add_command(label='增量备份')
    hymenu.add_cascade(label='备份策略', menu=bf_menu)
    huanyuan.add_command(label='完全还原', command=full_reduction)
    huanyuan.add_command(label='时间还原')
    # 绑定到一级菜单
    hymenu.add_cascade(label='还原方式', menu=huanyuan)
    menbar.add_cascade(label='功能', menu=hymenu)

    dmenu = Menu(menbar)  # 一级菜单

    dmenu.add_command(label='哈希验证', command=tool_hash)

    ctype_menu = Menu(root)  # 二级菜单
    ctype_menu.add_command(label='计算哈希值', command=hash_box)
    ctype_menu.add_command(label='加密 & 解密', command=crypt_box)
    ctype_menu.add_command(label='数字签名', command=signature_box)
    dmenu.add_command(label='随机密钥', command=random_key)
    dmenu.add_cascade(label='安全策略', menu=ctype_menu)
    menbar.add_cascade(label='工具', menu=dmenu)  # 一级菜单

    internet = Menu(menbar)
    internet.add_command(label='SSH')
    internet.add_command(label='SFTP')
    menbar.add_cascade(label='网络', menu=internet)

    hmenu = Menu(menbar)  # 关于 一级菜单
    hmenu.add_command(label='帮助', command=t_help)
    hmenu.add_command(label='关于本程序', command=about_main)
    menbar.add_cascade(label='关于', menu=hmenu)  # 一级菜单

    root['menu'] = menbar

    # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    aligner = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(aligner)
    root.mainloop()


if __name__ == "__main__":
    main()
