from os import path

python_shell = r'python'

aes_key_path = r'./backups'  # AES key save path
aes_encrypt_path = r'./backups'  # AES
# rsa_key_path = r'./backups'  # RSA
aes_decrypt_path = r'./backups'

db_table = 'datafile'
# time_folder = str(now_time())

data_path = r'./backups'
db_name = '文件资源管理器.db'
db_path = path.join(data_path, db_name)

# db_backup = r'./backups'
db_mode = """
        create table """ + db_table + """ (
            [id] integer PRIMARY KEY AUTOINCREMENT,
            file_path text,
            file_name text,
            c_time text,
            x_time text,
            now_time text,
            file_hash text
        )
"""

db_data = """
        insert into """ + db_table + """ 
            ( file_path, file_name, c_time, x_time, now_time, file_hash ) 
            values 
            (:file_path, :file_name, :c_time, :x_time, :now_time , :file_hash )        
"""
