"""
Python version:3.7 x64
OS: Windows10 x64
Pycharm version: 20.3
Github Index: https://github.com/zhaori


从阿拉伯数字、大小写英文字母、特殊符号打乱生成的随机密钥加上 随机token_bytes
"""
import base64
import secrets
from random import sample, shuffle
from string import digits, punctuation, ascii_letters


def create_key():
    str_number = sample(digits, 6)  # 0~9的阿拉伯数字
    str_punctuation = sample(punctuation, 16)  # 特殊字符32个
    str_other = sample(f"{digits}{ascii_letters}{punctuation}", 64)

    all_str_list = str_number + str_punctuation + str_other

    all_str_list = all_str_list + sample(digits, 8) + sample(punctuation, 16) + sample(
        f"{digits}{ascii_letters}{punctuation}", 18) + sample(digits, 6)
    shuffle(all_str_list)  # 打乱列表元素顺序
    key = ''.join(all_str_list)
    random_number = base64.encodebytes(secrets.token_bytes(90)).decode()
    return key + random_number


print(create_key())
