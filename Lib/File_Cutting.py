import os


class split_file(object):
    """
    大文件的切割和合并，应该提供一个分割后的小文件信息，以便断续合并
    read_size: 大小单位是字节，设定分割的文件大小默认是1024*1024 即 1mb
    del_cache: 默认为False，如果为True，会在合并完文件后删除小文件
    """

    def __init__(self, source, folder, outpath=None, read_size=None, del_cache=None):
        if read_size is None:
            read_size = 10 * 1024 * 1024
        if del_cache is None:
            del_cache = False
        if outpath is None:
            outpath = None

        self.read_size = read_size
        self.del_cache = del_cache
        self.file = source  # 分割文件，带路径的
        self.folder = folder  # 分割文件输出文件夹
        self.outfolder = outpath  # 合并输出文件，注意这里的参数应该是具体的文件名而非文件夹

    def excision(self):
        # 分割大文件
        sign = 0
        f = open(self.file, 'rb')
        while 1:
            file_value = f.read(self.read_size)
            if not file_value:
                break
            sign += 1
            filename = os.path.join(self.folder, f'temp00{sign}')
            outfile = open(filename, 'wb')
            outfile.write(file_value)
            outfile.close()
        f.close()

    @staticmethod
    def _write(file, data):
        # 写文件
        with open(file, 'ab') as f:
            f.write(data)

    @staticmethod
    def _read(file):
        # 读切割的小文件
        with open(file, 'rb') as f:
            return f.read()

    def _task_write(self, data):
        self._write(self.outfolder, self._read(data))

    def merge(self):
        # 合并小文件
        for i in os.listdir(self.folder):
            self._task_write(os.path.join(self.folder, i))
        if self.del_cache is False:
            pass
        elif self.del_cache:
            for f in os.listdir(self.folder):
                os.remove(os.path.join(self.folder, f))


if __name__ == '__main__':
    split_file(r'.\照片.zip', r'.\file_server\upload', r'.\3.zip').merge()
