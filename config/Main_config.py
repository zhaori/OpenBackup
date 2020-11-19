from ctypes import windll

tk_title = 'OpenBackup 0.0.1 beta'
logo = './pk.ico'

windll.shell32.SetCurrentProcessExplicitAppUserModelID('version')

listen_dir = [
    r"D:\OneDrive\Python\垃圾回收站\文件资源管理器",
    r"D:\OneDrive\Python\垃圾回收站\未知测试项"
]  # 监听文件夹
