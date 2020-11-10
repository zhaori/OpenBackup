"""
2020-11-08
CA数字证书颁发机构，使用RSA非对称加密算法，SQLite数据库存储
"""
import os

from rsa import newkeys, encrypt, decrypt, PrivateKey

from Lib.sqlite import Create_db

# ---------------------------------------------------SQLite数据库信息--------------------------------------------#
database = os.path.join('./', 'CA.db')
ca_table = 'CA_info'
target_table = 'target'
target_info_table = 'target_info'


def db_mode(table):
    if table == 'CA_info':
        mode = """
            create table {} (
                [id] integer PRIMARY KEY AUTOINCREMENT,
                country text,
                province text,
                city    text
                name    text,
                email   text
            )
        """.format(table)
        return mode

    elif table == 'target':
        mode = """
            create table {} (
                [id] integer PRIMARY KEY AUTOINCREMENT,
                name text,
                key text
            )
        """.format(table)
        return mode

    elif table == 'target_info':
        mode = """
            create table {} (
                [id] integer PRIMARY KEY AUTOINCREMENT,
                city    text
                name    text,
                email   text
            )
        """.format(table)
        return mode


def db_insert(table):
    if table == 'CA_info':
        insert = """
            insert into {}
                (country, province, city, name, email)
                values
                (:country, :province, :city, :name, :email)
        
        """.format(table)
        return insert

    elif table == 'target':
        insert = """
            insert into {}
                (name, key)
                values
                (:name, :key)

        """.format(table)
        return insert

    elif table == 'target_info':
        if table == 'CA_info':
            insert = """
                insert into {}
                    (city, name, email)
                    values
                    (:city, :name, :email)

            """.format(table)
            return insert


# db_table_list = [ca_table, target_table, target_info_table]

# for table in db_table_list:
#    Create_db(table, db_mode(table), db_insert(table), database).new_sql()


class PyOpenCA(object):
    """
    return:证书颁发
    """

    def __init__(self, key_path, file):
        self.file = file
        self.pubkey = os.path.join(key_path, "{}_pubkey.key".format(os.path.splitext(self.file)[0]))
        self.privkey = os.path.join(key_path, '{}_privkey.key'.format(os.path.splitext(self.file)[0]))

    @staticmethod
    def create_db(table_list: list):
        for table in table_list:
            Create_db(table, db_mode(table), db_insert(table), database).new_sql()

    def ca_encrypt(self, key_path):
        """
        key_path: 密钥存放路径
        """
        pubkey, privkey = newkeys(2048)
        with open(self.pubkey, "w+") as f1:
            f1.write(pubkey.save_pkcs1().decode())  # 公钥

        with open(self.privkey, "w+") as f2:
            f2.write(privkey.save_pkcs1().decode())  # 私钥

        with open(self.file, "r+", encoding='utf-8') as f3:
            message = f3.read()

        key_file = os.path.join(key_path, '{}.rsa'.format(self.file))
        with open(key_file, "wb") as f4:
            f4.write(encrypt(message.encode(), pubkey))

    def decrypt(self, encryption_path, name):
        """
        encryption_path: 密钥存放路径
        name: 加密文件
        """
        with open(self.privkey, "r") as f2:
            priv_key = PrivateKey.load_pkcs1(f2.read().encode())

        with open(name, "rb") as f3:
            mge = f3.read()

        un_rsa_key = decrypt(mge, priv_key).decode()
        key_file = os.path.join(encryption_path, name[0:-4])
        with open(key_file, "w+") as f4:
            f4.write(un_rsa_key)

    def get_ca(self, ca_info: dict, person_info: dict, pubkey, privkey, ca_path):
        """
        ca_info: CA证书机构信息
        person: 目标信息
        encryption: 公钥
        ca_path: CA证书存放路径
        return: 数字证书颁发，CA机构信息+目标信息+目标公钥
        """
        with open(privkey, "r") as f2:
            priv_key = PrivateKey.load_pkcs1(f2.read().encode())

        message = "{}\n {}\n {}\n".format(str(ca_info), str(person_info), str(priv_key))

        key_file = os.path.join(ca_path, '{}.rsa'.format(os.path.splitext(self.file)[0]))
        with open(key_file, "wb") as f4:
            f4.write(encrypt(message.encode(), pubkey))


if __name__ == "__main__":
    ca = PyOpenCA('./', './temp.json')
    # ca.ca_encrypt('./')
    ca.decrypt('./', './temp.json.rsa')
