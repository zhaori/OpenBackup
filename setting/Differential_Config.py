from Lib.Number_CN import *
from work.gettime import now_time

# ----------------------------数据库配置环境-------------------------#


df_db_table = num_cn(now_time())
time_folder = str(now_time())

# 建表

df_db_mode = """
        create table """ + df_db_table + """ (
            [id] integer PRIMARY KEY AUTOINCREMENT,
            mode text,
            difference text,
            source  text,
            reduce  text,
            now_time text
        )
"""

# 插入数据
df_db_data = """
        insert into """ + df_db_table + """ 
            (mode, difference, source, reduce, now_time) 
            values 
            (:mode, :difference, :source, :reduce, :now_time)        
"""
