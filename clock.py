from time import strftime, localtime, time, sleep

_time = 0


def countdown():
    # 倒计时
    global _time
    while 1:
        _time += 1
        print(_time)
        sleep(1)


def now_time():
    return strftime('%Y-%m-%d %H:%M:%S', localtime(time()))


# print(countdown())
