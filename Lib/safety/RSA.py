import os

from rsa import newkeys, encrypt, decrypt, PrivateKey


class RSA(object):
    """
     非对称加密类,同样拥有加密解密的方法一定要注意私钥的安全
    """

    def __init__(self, key_path, file_name):
        self.key_path = key_path  # key存放路径
        self.name = file_name  # 源文件名
        self.file = os.path.splitext(self.name)[0]  # 分离后的文件名，无后缀
        self.pubkey = os.path.join(self.key_path, "{}_pubkey.key".format(self.file))
        self.privkey = os.path.join(self.key_path, '{}_privkey.key'.format(self.file))

    def encrypt(self, crypt_path):
        # if 'pubkey.key' and 'privkey.key' not in os.listdir('./key'):
        # cryptfile是指加密后的文件 filname是加密前源文件
        # crypt_file = os.path.splitext(crypt_path)[0]
        pubkey, privkey = newkeys(2048)
        with open(self.pubkey, "w+") as f1:
            f1.write(pubkey.save_pkcs1().decode())  # 公钥

        with open(self.privkey, "w+") as f2:
            f2.write(privkey.save_pkcs1().decode())  # 私钥

        if '_privkey.key' and '_pubkey.key' in os.listdir('./'):
            os.remove('_privkey.key')
            os.remove('_pubkey.key')

        with open(self.name, "r+") as f3:
            message = f3.read()

        key_file = os.path.join(crypt_path, '{}.rsa'.format(self.file))
        with open(key_file, "wb") as f4:
            f4.write(encrypt(message.encode(), pubkey))

    def decrypt(self, crypt_path, name):
        with open(self.privkey, "r") as f2:
            priv_key = PrivateKey.load_pkcs1(f2.read().encode())

        with open(name, "rb") as f3:
            mge = f3.read()

        un_rsa_key = decrypt(mge, priv_key).decode()
        key_file = os.path.join(crypt_path, name[0:-4])
        with open(key_file, "w+") as f4:
            f4.write(un_rsa_key)
        # os.renames(key_file, key_file[])


if __name__ == "__main__":
    # rsa(r'..\..\Script', './help.pem', './help.key').encrypt(r'./help.pem')
    # r.encrypt('./')
    pass
