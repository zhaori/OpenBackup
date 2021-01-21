import os

from Lib.PyDOS import sys_copy
from config.Main_Config import READ_DB

temp_folder = r".\Temp"  # 临时文件夹
data_path = r'.\backups'  # 备份文件夹
basename_folder = os.path.basename(READ_DB)  # 不包含文件夹路径，只取文件夹名字

diff_backup = r'.\backups\TimeBackup\{}'.format(basename_folder)
copy_file = os.listdir(diff_backup)[-1]
filepath, file = os.path.split(copy_file)
sys_copy(os.path.join(diff_backup, copy_file), r'.\backups\incremental\{}\{}'.format(basename_folder, file))
