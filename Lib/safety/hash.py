import os
import secrets


class Hash(object):
    """
    计算哈希值
    """

    def __init__(self, data):
        self.data = data
        folder_path, file_name = os.path.split(self.data)
        # self.New_File_Name = os.path.splitext(file_name)[0]
        self.New_File_Name = file_name
        self.hash = None

    def md5(self):
        md = os.popen('{} dgst -md5 {}'.format('openssl', self.data))
        self.hash = md.read()[7 + len(self.data):]
        return self.hash

    def sha1(self):
        sa = os.popen('{} dgst -sha1 {}'.format('openssl', self.data))
        return str(sa.read()[10 + len(self.data):])

    def sha256(self):
        sa = os.popen('{} dgst -sha256 {}'.format('openssl', self.data))
        self.hash = sa.read()[10 + len(self.data):]
        return self.hash

    def sava_hash(self, file, suffix, path='./'):
        with open(os.path.join(path, '{}{}'.format(self.New_File_Name, suffix)), 'w') as f:
            f.write(file)


def Create_AESKey(byes: int):
    """
    生成随机口令
    """
    return str(secrets.token_hex(nbytes=byes))


def verify(old, new) -> bool:
    # 安全地比较两个字符串是否相等，以防暴力破解 返回布尔值
    return secrets.compare_digest(old, new)


if __name__ == "__main__":
    # print(Hash('.\Script', './temp.json').sha1())
    # pass
    h = Hash('../../help.txt')
    h.sava_hash(h.md5(), '.md5')
    # print(h.sha1())
    # h.sava_hash(h.sha1(),'.sha1', '../')
    # print(Create_AESKey(256))
