import os

from Lib.Number_CN import *
from gettime import now_time

# ----------------------------数据库配置环境-------------------------#


df_db_table = num_cn(now_time())
time_folder = str(now_time())

df_data_path = r'./ca_info'
df_db_name = 'snapshot.db'
df_db_path = os.path.join(df_data_path, df_db_name)

# 建表
# db_backup = r'./backups'
df_db_mode = """
        create table """ + df_db_table + """ (
            [id] integer PRIMARY KEY AUTOINCREMENT,
            difference text,
            reduce text,
            now_time text
        )
"""

# 插入数据
df_db_data = """
        insert into """ + df_db_table + """ 
            (difference, reduce, now_time) 
            values 
            (:difference, :reduce, :now_time)        
"""

# 找寻文件夹
search_path = r'D:\OneDrive\Python\垃圾回收站\文件资源管理器'
