import os


class AES(object):
    """
    AES加密解密类,手动指定 openssl.exe绝对路径或相对路径
    """

    def __init__(self, file, pwd):
        self.text = file
        self.password = pwd
        folder_path, file_name = os.path.split(self.text)
        self.New_File_Name = '{}_{}'.format(os.path.splitext(file_name)[0], os.path.splitext(file_name)[1][1:])

    def encrypt(self, out_path='./'):
        # 对称加密
        o_path = os.path.join(out_path, '{}.file'.format(self.New_File_Name))
        try:
            os.system("{} enc -aes-256-cbc -e -in {} -out {} -pass pass:{}"
                      .format('openssl', self.text, o_path, self.password))
        except FileNotFoundError as e:
            print(e)

    def decrypt(self, in_path, out_path='./'):
        # 对称解密
        # path = os.path.join(in_path, self.text)
        # out_path = os.path.join(on_path, self.text)

        out_file = os.path.splitext(in_path)[0]
        file = '{}.{}'.format(out_file[0:out_file.find('_')], out_file[out_file.find('_') + 1:])
        os.system("{} enc -aes-256-cbc -d -in {} -out {} -pass pass:{}"
                  .format('openssl', in_path,
                          os.path.join(out_path, file), self.password))

    def sava_key(self):
        with open('{}.key'.format(self.New_File_Name), 'w') as k:
            k.write(self.password)


if __name__ == "__main__":
    # os.chdir('../')
    a = AES('../help.txt', '123456')
    a.encrypt('../')
    # db_full.sava_key()
    # db_full.decrypt('../help.file', '../help.json')
