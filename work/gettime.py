from time import strftime, localtime, time, sleep


def countdown(sec):
    # 倒计时
    sleep(sec)
    return True


def now_time():
    # 返回的是年月日分
    return strftime('%Y%m%d%H%M', localtime(time()))


def now_time_s():
    # 返回的是年月日分秒
    return strftime('%Y%m%d%H%M%S', localtime(time()))
