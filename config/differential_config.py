from Lib.Number_CN import *
from gettime import now_time

# ----------------------------数据库配置环境-------------------------#


df_db_table = num_cn(now_time())
time_folder = str(now_time())



# 建表

df_db_mode = """
        create table """ + df_db_table + """ (
            [id] integer PRIMARY KEY AUTOINCREMENT,
            difference text,
            now_time text
        )
"""

# 插入数据
df_db_data = """
        insert into """ + df_db_table + """ 
            (difference, now_time) 
            values 
            (:difference, :now_time)        
"""

