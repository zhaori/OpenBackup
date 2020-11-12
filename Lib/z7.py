import os

"""
参数 -mx
0复制无压缩。
1 LZMA 64 KB 32 HC4 BCJ最快的压缩
3 LZMA 1 MB 32 HC4 BCJ快速压缩
5 LZMA 16 MB 32 BT4 BCJ正常压缩
7 LZMA 32 MB 64 BT4 BCJ最大压缩
9 LZMA 64 MB 64 BT4 BCJ2超压缩-mdNm
-mmt 开启多线程模式
"""


class archive(object):

    def __init__(self, folder, source):
        self.source = source  # 压缩源目录
        self.folder = folder  # 压缩文件存放目录
        self.script = '7z'

    def seven_zip(self, filename, option=0):
        # filename 压缩包名，无需后缀
        file = os.path.join(self.folder, filename)
        if option == 0:
            os.system(r'{} -mx5 -t7z a {} {} -mmt'.format(self.script, file, self.source))
        elif option == 1:
            # 压缩并删除源文件
            os.system(r'{} -mx5 -t7z a {} {} -mmt -sdel'.format(self.script, file, self.source))

    def unzip(self, path, destination):
        """
        path: 压缩包路径
        destination：解压目的地
        return: 解压目的文件夹可以不存在，如不存在自动创建
        """
        os.system(r'{} x {} -y -aos -o{}'.format(self.script, path, destination))


if __name__ == "__main__":
    w = archive(r'C:/Users/zgz/Documents/Pycharm-workspace', 'C:/Users/zgz/Documents/Pycharm-workspace/垃圾回收站/back/*')
    w.seven_zip('废品站')
    # w.unzip('./废品站.7z', 'C:/Users/zgz/Desktop/111/')
