from ctypes import windll
from os import path

# from gettime import now_time

tk_title = 'OpenBackup 0.0.1 beta'
logo = './pk.ico'

windll.shell32.SetCurrentProcessExplicitAppUserModelID('version')

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

search_path = [
    r'D:\Pycharm-workspace\垃圾回收站\文件资源管理器'
]

# dict ca_info type
ignore_file_name = None
ignore_file_size = None

"""
"""
# p_j = PyJson('temp.json')
# os.mkdir(time_folder)
# new_zip = archive(time_folder, p_j.read('folder'))
# new_zip.seven_zip(time_folder)
"""
"""
