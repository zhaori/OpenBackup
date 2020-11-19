import os
from tkinter import Tk, Button
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
#from Lib.Error import show_error
from Lib.safety.AES import AES
from Lib.safety.RSA import RSA
from Lib.safety.Hash import Create_AESKey
from config.db_config import *
from config.Main_config import windll, tk_title, logo

# ------------------------------------加密--------------------------------#
def crypt_box():
    win = Tk()  # 构造窗体
    windll.shell32.SetCurrentProcessExplicitAppUserModelID('version')  # 任务栏图标
    aes_key = os.path.join(aes_key_path, 'key')

    def get_aes_key():
        if 'key' in os.listdir(aes_key_path):
            showerror('错误提示', 'key文件已存在，请删除后再重试')
        else:
            with open(aes_key, 'w') as f:
                f.write(Create_AESKey(64))

    def aes_encrypt():
        # AES 加密，根据加密文件大小决定加密速度
        filename = str(askopenfilename(title='打开文件'))
        folder_path, file_name = os.path.split(filename)
        new_key_name = "{}".format(os.path.join(folder_path, '{}.key'.format(file_name)))
        os.renames(aes_key, new_key_name)
        try:
            with open(new_key_name, 'r') as k:
                key = k.read()
            a = AES(filename, key)
            a.encrypt(out_path=folder_path)
        except FileNotFoundError as e:
            show_error(e)

    def aes_decrypt():
        encrypt_file = str(askopenfilename(title='解密文件', filetypes=([('file', '.file')])))  # 打开加密文件
        key_file = askopenfilename(title='打开AES密钥', filetypes=([('key', '.key')]))
        try:
            with open(key_file, 'r') as k:
                key = k.read()
            a = AES(encrypt_file, key)
            a.decrypt(encrypt_file, '{}.de'.format(os.path.splitext(encrypt_file)[0]))
        except FileNotFoundError as e:
            show_error(e)

    def rsa_encrypt():
        filename = str(askopenfilename(title='打开文件'))
        rsa_key = askopenfilename(title='打开RSA密钥', filetypes=([('key', '.key')]))
        try:
            r = RSA(rsa_key, filename)
            r.encrypt(rsa_key)
        except FileNotFoundError:
            show_error('未找到公钥文件或取消了执行')

    def rsa_decrypt():
        filename = str(askopenfilename(title='打开文件', filetypes=([('rsa', '.rsa')])))
        rsa_key = askopenfilename(title='打开RSA密钥', filetypes=([('key', '.key')]))
        try:
            r = RSA(rsa_key, filename)
            r.decrypt(rsa_key, filename)
        except FileNotFoundError:
            show_error('未找到私钥文件取消了执行')

    _title = '加密&解密'
    width = 280
    height = 250
    win.title(tk_title)
    win.iconbitmap(logo)

    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    aligner = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    win.geometry(aligner)

    Button(win, text='生成AES KEY', command=get_aes_key).place(relx=0.36, rely=0.08, width=90, height=40)
    Button(win, text='AES加密', command=aes_encrypt).place(relx=0.06, rely=0.4, width=90, height=40)
    Button(win, text='AES解密', command=aes_decrypt).place(relx=0.58, rely=0.4, width=90, height=40)
    Button(win, text='RSA加密', command=rsa_encrypt).place(relx=0.05, rely=0.7, width=90, height=40)
    Button(win, text='RSA解密', command=rsa_decrypt).place(relx=0.586, rely=0.7, width=90, height=40)
    win.mainloop()


if __name__ == "__main__":
    # crypt_box()
    pass
