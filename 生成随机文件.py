import getpass
import os
import time


# 生成指定大小的TXT档
def generate_file():
    file_size = 0
    # 判断输入是否有误
    while True:
        size = input('请输入你想生成的TXT文件大小(MB):')
        if not size.strip().isdigit():
            print('只能输入整数，请重新输入!')
            continue
        else:
            file_size = int(size)
            break
    if file_size >= 200:
        print('正在生成TXT文件，请稍候... ...')
    # 生成指定大小的TXT档

    filepath = f'C:\\Users\\{getpass.getuser()}\\Desktop\\'
    f = open(os.path.join(filepath, '测试文件.txt'), 'w+')
    # 获取开始时间
    start_clock = time.perf_counter()
    for i in range(file_size):
        if i >= 100:
            if i % 100 == 0:
                print(f'已生成{i // 100 * 100}MB数据.')
        for j in range(1024):
            try:
                f.write('01' * 512)
            except KeyboardInterrupt:
                print('\n异常中断:KeyboardInterrupt')
                f.close()
                exit(-1)
    f.close()
    print(f'文件已成生并保存在桌面,  文件大小:{file_size}MB.\n')
    print(f'总共耗时:{(time.perf_counter() - start_clock):<.3}sec.')


if __name__ == '__main__':
    generate_file()
