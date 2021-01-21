import os
from tkinter.filedialog import askopenfilename


def open_take():
    # 修改任务文件
    temp_file = askopenfilename(title='打开json任务文件', filetypes=([('json', '.json')]))
    os.system('{} {}'.format('notepad', temp_file))
