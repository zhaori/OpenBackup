import os
from threading import Thread
from tkinter import Menu, Tk

from config.Main_Config import about_main, read_help, tk_title, logo, ssh_options
from config.Net_Config import host
from update import update_file
from work import *


def get_listen_info():
    def run():
        os.popen(r'watch_listen.exe')

    Thread(target=run).start()


def ping_network():
    os.system(f'ping {host}')


class OpenBackup(object):

    def __init__(self):
        self.root = Tk()
        self.width = 550
        self.height = 400
        self.root.title(tk_title)
        self.root.iconbitmap(logo)

        # 居中
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        self.aligner = '%dx%d+%d+%d' % (
            self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)

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
        self.transmit = Menu(self.root)

    def _quit(self):
        self.root.quit()
        self.root.destroy()
        exit()

    def _menu(self):
        # --------文件--------#
        self.wj.add_command(label='新建任务', command=new_task)
        self.wj.add_command(label='加载任务', command=open_tasks)
        self.wj.add_command(label='删除任务', command=task_delete)
        self.wj.add_separator()

        self.wj.add_command(label='退出', command=self._quit)
        self.menbar.add_cascade(label='文件', menu=self.wj)  # 绑定到一级菜单

        # --------功能--------#
        self.bf.add_command(label='完全备份', command=full_backup)
        self.bf.add_command(label='差异备份', command=differ_backup)
        self.bf.add_command(label='增量备份', command=incremental_backup)
        self.bf.add_command(label='文件快照', command=get_listen_info)
        self.gn.add_cascade(label='备份策略', menu=self.bf)
        self.huanyuan.add_command(label='完全还原', command=full_reduction)
        self.huanyuan.add_command(label='时光回溯', command=recovery_run)

        self.gn.add_cascade(label='还原方式', menu=self.huanyuan)
        self.gn.add_cascade(label='计划任务')
        self.menbar.add_cascade(label='功能', menu=self.gn)

        # --------工具--------#
        self.gj.add_command(label='哈希验证', command=tool_hash)
        self.gj.add_command(label='计算哈希值', command=hash_box)
        self.gj.add_command(label='加密 & 解密', command=crypt_box)
        self.gj.add_command(label='数字签名', command=signature_box)
        self.menbar.add_cascade(label='工具', menu=self.gj)

        # --------网络--------#
        self.net.add_command(label="PING", command=ping_network)
        self.net.add_command(label="设置", command=ssh_options)
        self.net.add_command(label="上传", command=Transmit().up)
        self.net.add_command(label="下载", command=Transmit().down)
        self.net.add_cascade(label='自动任务', menu=self.transmit)

        self.net.add_command(label='历史记录', command=open_record)
        self.net.add_command(label='清空记录', command=del_history)
        self.transmit.add_command(label='开始同步', command=run_automation)
        self.transmit.add_command(label='终止同步', command=stop)
        self.menbar.add_cascade(label='同步', menu=self.net)

        # --------帮助--------#
        self.help.add_command(label='帮助', command=read_help)
        self.help.add_command(label='更新', command=update_file)
        self.help.add_command(label='关于本程序', command=about_main)
        self.menbar.add_cascade(label='关于', menu=self.help)

    def create_win(self):
        self._menu()
        self.root['menu'] = self.menbar

        self.root.geometry(self.aligner)
        self.root.mainloop()


if __name__ == '__main__':
    OpenBackup().create_win()
