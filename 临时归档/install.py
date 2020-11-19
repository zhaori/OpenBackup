import os

# import platform

# os_name = platform.system()
package_list = ['rsa', 'watchdog', 'pymongo']
# package_list = ['pyqt5', 'PyQt5-tools', 'PyQtWebEngine', 'PyQtChart', 'QScintilla']
# package_list = ['redis==2.10.6', 'rsa']
# package_list = ['pyinstaller']
# package_list = ['cryptography']
# print(os_name)

for s_name in package_list:
    os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple %s' % s_name)

# python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --upgrade pip
# pypy -m pip install
