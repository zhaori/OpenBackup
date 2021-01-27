import json
import os
from tkinter.messagebox import showinfo, askokcancel
from urllib.request import urlretrieve

from Lib.super_json import SuperJSON
from Lib.z7 import archive

"""
根目录下的version文件代表当前程序的版本号，update.json代表的是从远程更新下的更新配置文件，代表着最新版本号及下载链接
"""
update_ini = 'https://zhaori.github.io/update/OpenBackup/update.json'


def get_file(url, path=None):
    """
    下载文件，url是文件下载的直连网址，默认下载到根目录
    """
    if path is None:
        path = './'
    urlretrieve(url, os.path.join(path, os.path.basename(url)))


def read_json(json_file):
    with open(json_file, 'r', encoding="utf-8") as f:
        return dict(json.loads(f.read()))


def upgrade(file):
    archive.unzip(file, r"./")


def update_file():

    get_file(update_ini)

    # 解析update.json里的程序更新信息
    j = SuperJSON('update.json')
    v = j.search_value("Python", "OpenBackup", "version")

    with open("version", "r", encoding="utf-8") as f:
        _version = f.read()
    if _version == v:
        showinfo("升级信息", "版本一致无需更新")

    elif _version < v:
        if askokcancel("升级信息", "有最新版本可下载，是否更新？"):
            get_file(j.search_value("Python", "OpenBackup", "update"))
            upgrade(j.search_value("Python", "OpenBackup", "file"))
        else:
            exit()
