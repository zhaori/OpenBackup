import os

from rsa import PrivateKey, sign, PublicKey, verify, pkcs1


class Signature(object):
    """
    这是数字签名类，sign是签名，verify是验证，使用前必须保证文件已经加密结束
    私钥签名，公钥验证
    """

    def __init__(self, hash_file):
        """
        self._hash: 指定签名哈希算法，可选为MD5、SHA-1、SHA-256、SHA-512
        """
        file = os.path.splitext(hash_file)[0]
        self.file_path, self.hash_file = os.path.split(os.path.abspath(hash_file))  # 哈希文件名
        # self.hash_file = hash_file

        self.sha = os.path.join(self.file_path, "{}.sign".format(file))  # 数字签名后保存的签名文件名

    def sign(self, privkey):
        """
        privkey: 私钥
        """
        with open(privkey, "r")as f1:
            priv_key = PrivateKey.load_pkcs1(f1.read().encode())

        with open(self.hash_file, 'rb') as f:
            mess = f.read()

        with open(self.sha, 'wb') as f:
            f.write(sign(mess, priv_key, 'SHA-256'))

    def verify(self, pubkey):
        """
        pubkey: 公钥
        """
        with open(pubkey, 'r') as f1:
            pub_key = PublicKey.load_pkcs1(f1.read().encode())

        with open(self.hash_file, 'rb') as f:
            mess = f.read()

        with open(self.sha, 'rb') as f:
            s_sign = f.read()
        try:
            ver = verify(mess, s_sign, pub_key)
            print('验证成功,使用的哈希算法是：%s' % ver)
        except pkcs1.VerificationError:
            print('验证不通过')


if __name__ == '__main__':
    s = Signature('./help.rsa')
    # self.sign('./help_privkey.key')
    s.verify('./help_pubkey.key')
