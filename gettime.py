from time import strftime, localtime, time, sleep


def countdown(sec):
    # 倒计时
    sleep(sec)
    return True


def now_time():
    return strftime('%Y%m%d%H%M', localtime(time()))
