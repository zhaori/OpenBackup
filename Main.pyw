import os
from tkinter import Menu, Tk, Text, END, INSERT, PhotoImage
from threading import Thread
from setting.Main_Config import tk_title, logo
from work import *
from setting.Main_Config import about_main, read_help
from work.transmit import open_record, del_history, Transmit

os.system(f'path=%path%;{os.path.abspath("./Script")}')

def random_key_main():
    # 此处如果使用的是os.system或者用的是subprocess运行程序都会阻塞主进程导致无法使用其它功能
    # 同时，random_key无法像其它模块能够直接通过Main引用，因此编译成exe可执行文件运行
    os.popen(r'random_key.exe')


def get_listen_info():
    def run():
        os.system(r'watch_listen.exe')

    Thread(target=run).start()


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
        text.insert(INSERT, open('./LICENSE', encoding='utf-8').read())

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

        # 图标设置
        self.shang_chuan = PhotoImage(file='.\logo\上传.gif')
        self.xia_zai = PhotoImage(file='.\logo\下载.gif')
        self.guan_yu = PhotoImage(file='.\logo\关于.gif')
        self.tong_bu = PhotoImage(file='.\logo\同步.gif')
        self.zeng_liang_bei_fen = PhotoImage(file='.\logo\增量备份.gif')
        self.shou_hu_jin_cheng = PhotoImage(file='.\logo\守护.gif')
        self.shui_ji_mi_yao = PhotoImage(file='.\logo\密钥.gif')
        self.bang_zhu = PhotoImage(file='.\logo\帮助.gif')
        self.kuai_zhao = PhotoImage(file='.\logo\快照.gif')
        self.shu_ju_jia_mi = PhotoImage(file='.\logo\数据加密.gif')
        self.zeng_liang_hui_fu = PhotoImage(file='.\logo\时光机器.gif')
        self.jian_kong_wen_jian_xi_tong = PhotoImage(file='.\logo\监控.gif')
        self.ying_pan = PhotoImage(file='.\logo\硬盘.gif')
        self.ying_pan_fu_zhi = PhotoImage(file='.\logo\硬盘复制.gif')
        self.shu_zi_qian_ming = PhotoImage(file='.\logo\签名.gif')
        self.ji_hua_ren_wu = PhotoImage(file='.\logo\计划.gif')
        self.ji_shuan_ha_xi = PhotoImage(file='.\logo\计算.gif')
        self.huan_yuan = PhotoImage(file='.\logo\还原.gif')
        self.tui_chu = PhotoImage(file=r'.\logo\退出.gif')
        self.yan_zheng = PhotoImage(file='.\logo\验证.gif')
        self.cha_yi_bei_fen = PhotoImage(file='.\logo\差异.gif')
        self.che_lue = PhotoImage(file='.\logo\策略.gif')

    def _quit(self):
        self.root.quit()
        self.root.destroy()
        exit()

    def _menu(self):
        # --------文件--------#
        self.wj.add_command(label='新建任务', command=new_task)
        self.wj.add_command(label='修改任务', command=open_take)
        self.wj.add_command(label='加载任务', command=open_tasks)
        self.wj.add_separator()

        self.wj.add_command(label='退出', command=self._quit, image=self.tui_chu, compound='left')
        self.menbar.add_cascade(label='文件', menu=self.wj)  # 绑定到一级菜单

        # --------功能--------#
        self.bf.add_command(label='完全备份', command=full_backup, image=self.ying_pan_fu_zhi, compound='left')
        self.bf.add_command(label='差异备份', command=differ_backup, image=self.cha_yi_bei_fen, compound='left')
        self.bf.add_command(label='增量备份', command=incremental_backup, image=self.zeng_liang_bei_fen, compound='left')
        self.bf.add_command(label='文件快照', command=get_listen_info, image=self.kuai_zhao, compound='left')
        self.gn.add_cascade(label='备份策略', menu=self.bf, image=self.che_lue, compound='left')
        self.huanyuan.add_command(label='完全还原', command=full_reduction, image=self.huan_yuan, compound='left')
        self.huanyuan.add_command(label='时光回溯', command=recovery_run, image=self.zeng_liang_hui_fu, compound='left')

        self.gn.add_cascade(label='还原方式', menu=self.huanyuan, image=self.huan_yuan, compound='left')
        self.gn.add_cascade(label='计划任务', image=self.ji_hua_ren_wu, compound='left')
        self.menbar.add_cascade(label='功能', menu=self.gn)

        # --------工具--------#
        self.gj.add_command(label='哈希验证', command=tool_hash, image=self.yan_zheng, compound='left')
        self.gj.add_command(label='随机密钥', command=random_key_main, image=self.shui_ji_mi_yao, compound='left')
        self.gj.add_cascade(label='安全策略', menu=self.ctype_menu, image=self.che_lue, compound='left')
        self.ctype_menu.add_command(label='计算哈希值', command=hash_box, image=self.ji_shuan_ha_xi, compound='left')
        self.ctype_menu.add_command(label='加密 & 解密', command=crypt_box, image=self.shu_ju_jia_mi, compound='left')
        self.ctype_menu.add_command(label='数字签名', command=signature_box, image=self.shu_zi_qian_ming, compound='left')
        self.menbar.add_cascade(label='工具', menu=self.gj)

        # --------网络--------#
        self.net.add_command(label="上传", command=Transmit().up)
        self.net.add_command(label="下载", command=Transmit().down)
        # self.net.add_cascade(label='自动', menu=self.transmit)

        self.net.add_command(label='历史记录', command=open_record)
        self.net.add_command(label='清空记录', command=del_history)
        # self.transmit.add_command(label='开始同步', command=run_automation)
        # self.transmit.add_command(label='终止同步', command=os._exit)
        self.menbar.add_cascade(label='同步', menu=self.net)

        # --------帮助--------#
        self.help.add_command(label='帮助', command=read_help, image=self.bang_zhu, compound='left')
        self.help.add_command(label='关于本程序', command=about_main, image=self.guan_yu, compound='left')
        self.menbar.add_cascade(label='关于', menu=self.help)

    def create_win(self):
        self._menu()
        self.root['menu'] = self.menbar

        self.root.geometry(self.aligner)
        self.root.mainloop()


if __name__ == '__main__':
    from work.differ_backup import differ_backup
    differ_backup()
