import os
from tkinter.filedialog import askopenfilename


def open_config():
    # 修改配置文件
    temp_file = askopenfilename(title='打开config配置文件', filetypes=([('py', '.py')]))
    os.system('{} {}'.format('notepad', temp_file))


open_config()
