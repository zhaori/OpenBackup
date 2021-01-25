python_shell = r'python'

aes_key_path = r'./backups'  # AES key save path
aes_encrypt_path = r'./backups'  # AES
aes_decrypt_path = r'./backups'

db_table = 'datafile'
data_path = r'./backups'
db_backup = r'./backups'

db_mode = f"""
        create table {db_table} (
            [id] integer PRIMARY KEY AUTOINCREMENT,
            file_path text,
            file_name text,
            c_time text,
            m_time text,
            now_time text,
            file_hash text
        )
"""

db_data = f"""
        insert into {db_table} 
            ( file_path, file_name, c_time, m_time, now_time, file_hash ) 
            values 
            (:file_path, :file_name, :c_time, :m_time, :now_time , :file_hash )        
"""
