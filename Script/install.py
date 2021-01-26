import os
import sys
from threading import Thread


class VersionError(Exception):
    def __init__(self, *args, **kwargs):
        pass

    def __str__(self):
        return 'Python Version not is 2'


for version in sys.version_info[0:1]:
    if version == 2:
        raise VersionError
    else:
        pass


class Py_install(object):
    def __init__(self):
        # 'gevent'
        self.package_list = ['rsa',
                             'pymongo==3.11.2',
                             'pywin32',
                             'paramiko',
                             'pyinstaller'
                             ]
        self.install_list = [Thread(target=self.__install_page, args=(s,)) for s in self.package_list]
        self.uninstall_list = [Thread(target=self.__uninstall_page, args=(s,)) for s in self.package_list]

    @staticmethod
    def __install_page(s_name):
        os.system(f'python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple {s_name}')

    @staticmethod
    def __uninstall_page(s_name):
        os.system(f'python -m pip uninstall {s_name} -y')

    def install(self):
        for p in self.install_list:
            p.start()
        for i in self.install_list:
            i.join()

    def uninstall(self):
        for p in self.uninstall_list:
            p.start()
        for i in self.uninstall_list:
            i.join()


def upgrade_pip():
    os.system('python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --upgrade pip')


if __name__ == '__main__':
    upgrade_pip()
    Py_install().install()

# package_list = ['pyqt5', 'PyQt5-tools', 'PyQtWebEngine', 'PyQtChart', 'QScintilla']
# package_list = ['redis==2.10.6', 'rsa']
# package_list = ['pyinstaller']
# package_list = ['cryptography']
