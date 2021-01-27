import os

"""
:compile_list 编译文件的路径
"""

os.system("pyinstaller -F Main.pyw -i main.ico --noconsole")
