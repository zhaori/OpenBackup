import os
from tkinter import Menu, Tk, Text, END, INSERT
from tkinter.messagebox import showinfo

from work import *
from config.Main_config import tk_title, logo

os.system('path=%path%;./')


def about_main():
    showinfo(tk_title, '        本程序遵守GPL 3.0协议开源\n '
                       '                 @ Python3.7  \n '
                       ' https://github.com/zhaori/OpenBackup')


def t_help():
    os.system(r'help.txt')


def random_key():
    os.system(r'python work\random_key.py')


class Openbackup(object):

    def __init__(self):
        self.root = Tk()
        self.width = 499
        self.height = 338
        self.root.title(tk_title)
        self.root.iconbitmap(logo)
        text = Text(self.root)
        text.grid(row=2, column=2, columnspan=6, rowspan=15)

        # 获取数据
        # 填充到text控件
        text.delete(1.0, END)
        text.insert(INSERT, open('./doc/LICENSE', encoding='utf-8').read())
        # 居中

        # 菜单
        self.menbar = Menu(self.root)  # 根
        self.wj = Menu(self.menbar)  # 文件，绑定到根
        self.gn = Menu(self.menbar)  # 功能，绑定到根
        self.gj = Menu(self.menbar)  # 工具，绑定到根
        self.net = Menu(self.menbar)  # 网络，绑定到根
        self.help = Menu(self.menbar)  # 帮助，绑定到根
        # 二级菜单
        self.bf = Menu(self.root)
        self.huanyuan = Menu(self.root)
        self.ctype_menu = Menu(self.root)

    def _quit(self):
        self.root.quit()
        self.root.destroy()
        exit()

    def window_menu(self):
        # --------文件--------#
        self.wj.add_command(label='新建任务', command=new_task)
        self.wj.add_command(label='修改任务', command=open_take)
        self.wj.add_command(label='修改配置', command=open_config)
        self.wj.add_separator()

        self.wj.add_command(label='退出', command=self._quit)
        self.menbar.add_cascade(label='文件', menu=self.wj)  # 绑定到一级菜单

        # --------功能--------#
        self.bf.add_command(label='差异备份')
        self.bf.add_command(label='增量备份')
        self.gn.add_cascade(label='备份策略', menu=self.bf)
        self.huanyuan.add_command(label='完全还原', command=full_reduction)
        self.huanyuan.add_command(label='时光回溯')

        self.gn.add_cascade(label='还原方式', menu=self.huanyuan)
        self.gn.add_cascade(label='计划任务')
        self.menbar.add_cascade(label='功能', menu=self.gn)

        # --------工具--------#
        self.gj.add_command(label='哈希验证', command=tool_hash)
        self.gj.add_command(label='随机密钥', command=random_key)
        self.gj.add_cascade(label='安全策略', menu=self.ctype_menu)
        self.ctype_menu.add_command(label='计算哈希值', command=hash_box)
        self.ctype_menu.add_command(label='加密 & 解密', command=crypt_box)
        self.ctype_menu.add_command(label='数字签名', command=signature_box)
        self.menbar.add_cascade(label='工具', menu=self.gj)

        # --------网络--------#
        self.net.add_command(label='SSH')
        self.net.add_command(label='SFTP')
        self.menbar.add_cascade(label='网络', menu=self.net)

        # --------帮助--------#
        self.help.add_command(label='帮助', command=t_help)
        self.help.add_command(label='关于本程序', command=about_main)
        self.menbar.add_cascade(label='关于', menu=self.help)

        self.root['menu'] = self.menbar

        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        aligner = '%dx%d+%d+%d' % (
            self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.root.geometry(aligner)
        self.root.mainloop()


if __name__ == '__main__':
    Openbackup().window_menu()
