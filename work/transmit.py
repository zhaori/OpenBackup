import os
from Lib.PySSH import PySFTP
from Lib.z7 import archive
from setting.Main_Config import READ_DB
from setting.Net_Config import serverpath, transmit_time
import subprocess
from setting.MongoDB_Config import mongo_host, mongo_port
from Lib.MongoDBSever import Mongodb_server
from tkinter import Tk, StringVar
from tkinter.messagebox import showinfo
from tkinter.ttk import Combobox
from setting.Main_Config import logo
from work.gettime import now_time_s
from time import sleep

pid = None


class Transmit(object):

    def __init__(self):
        self.zip_temp = './Temp'
        self.folder_file = os.path.basename(READ_DB)
        self.compressed_files = os.path.join(self.zip_temp, f'{self.folder_file}.7z').replace('/', '\\')  # 在Temp文件夹的压缩包
        self.server_file = os.path.join(serverpath, f'{self.folder_file}.7z').replace('\\', '/')  # 在服务器的压缩包

    def up(self):
        # 压缩文件夹并上传
        new_zip = archive(self.zip_temp, READ_DB)
        new_zip.seven_zip(self.folder_file)
        PySFTP().sftp_up(self.compressed_files, self.server_file)
        data = {
            'local': READ_DB,
            'source': self.compressed_files,
            'destination': self.server_file,
            'handle': 'uploading'
        }
        Mongodb_server(mongo_host, mongo_port).insert('log', now_time_s(), data)
        showinfo('提示', '上传成功')

    def down(self):
        PySFTP().sftp_down(self.server_file, self.compressed_files)
        data = {
            'local': READ_DB,
            'source': self.compressed_files,
            'destination': self.server_file,
            'handle': 'download'
        }
        Mongodb_server(mongo_host, mongo_port).insert('log', now_time_s(), data)
        archive.unzip(self.compressed_files, READ_DB)
        showinfo('提示', '下载成功')

    @staticmethod
    def arg_down(server, clint, source):
        # 传参下载
        PySFTP().sftp_down(server, clint)
        archive.unzip(clint, source)

    def _up_down(self):
        # 上传和下载
        archive(self.zip_temp, READ_DB).seven_zip(self.folder_file)
        sftp = PySFTP()
        Mongodb_server(mongo_host, mongo_port).insert("log", "automation", {'time': now_time_s(), 'handle': '上传'})
        sftp.sftp_up(self.compressed_files, self.server_file)
        sftp.sftp_down(self.server_file, self.compressed_files)
        Mongodb_server(mongo_host, mongo_port).insert("log", "automation", {'time': now_time_s(), 'handle': '下载'})
        archive.unzip(self.compressed_files, READ_DB)
        Transmit().clean_temp()

    def automation(self):
        with open(f'{os.getpid()}.pid', 'w') as f:
            f.write('')
        while 1:
            if transmit_time is None:
                self._up_down()
                sleep(60)
            elif not transmit_time is None:
                self._up_down()
                sleep(transmit_time)

    def sys_pid(self):
        return self.pid

    #def clean_temp(self):
    #    os.remove(self.compressed_files)


def run_automation():
    # Process(target=Transmit().automation).start()
    subprocess.run('./automation.exe')


def stop():
    pass


def del_history():
    # 删除自动传输的log集合
    Mongodb_server(mongo_host, mongo_port).del_table('log')


def get_db_table():
    return Mongodb_server(mongo_host, mongo_port).search_table('log')


class history_record(object):
    def __init__(self):
        self.win = Tk()
        self.width = 250
        self.height = 200
        self.win.title('历史记录')

        # self.win.iconbitmap(logo)
        screenwidth = self.win.winfo_screenwidth()
        screenheight = self.win.winfo_screenheight()
        aligner = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth - self.width) / 2,
                                   (screenheight - self.height) / 2)
        self.win.geometry(aligner)
        self.db = Mongodb_server(mongo_host, mongo_port)

    def handle(self, *args):
        return self.db.search_one(f"record", self.comboxlist.get(),
                                  {"_id": 0, "destination": 1, "local": 1, "source": 1})

    @staticmethod
    def _db_record():
        return {"_id": 0, "destination": 1, "local": 1, "source": 1}

    def _exit_win(self):
        self.win.quit()

    def ok(self):
        Transmit().arg_down(self.handle()['destination'], self.handle()['source'], self.handle()['local'])
        showinfo('提示', '还原成功')
        self._exit_win()

    def del_data(self):
        self.db.del_key('record', self.comboxlist.get(), self._db_record())
        exit()

    def _win(self):
        time_list = []
        comvalue = StringVar()  # 窗体自带的文本，新建一个值
        self.comboxlist = Combobox(self.win, textvariable=comvalue, state='readonly')  # 初始化
        for get_time in get_db_table():
            time_list.append(
                f"{get_time[0:4]}-{get_time[4:6]}-{get_time[6:8]} {get_time[8:10]}:{get_time[10:12]}:{get_time[12:14]}"
            )
        self.comboxlist["values"] = tuple(time_list)
        self.comboxlist.current(0)  # 选择第一个

        self.comboxlist.bind("<<ComboboxSelected>>", self.handle)  # 绑定事件,(下拉列表框被选中时，绑定handle()函数)
        self.comboxlist.place(relx=0.2, rely=0.25, width=150, height=40)

    def Main(self):
        self._win()
        # Button(self.win, text='确定', command=self.ok).place(relx=0.05, rely=0.75, width=70, height=30)
        # Button(self.win, text='删除', command=self.del_data).place(relx=0.36, rely=0.75, width=70, height=30)
        # Button(self.win, text='取消', command=self._exit_win).place(relx=0.68, rely=0.75, width=70, height=30)
        self.win.mainloop()


def open_record():
    # 加载配置文件
    history_record().Main()


if __name__ == '__main__':
    run_automation()
    # print(get_db_table())
