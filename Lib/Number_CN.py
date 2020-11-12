# 阿拉伯数字与中文转换 20201022
def num_cn(n) -> str:
    """
    return: 传入参数可以是int或 str
    """
    num_dict = {
        '0': '零',
        '1': '一',
        '2': '二',
        '3': '三',
        '4': '四',
        '5': '五',
        '6': '六',
        '7': '七',
        '8': '八',
        '9': '九',
    }
    num_for_cn = []
    for i in str(n):
        if i in num_dict.keys():
            num_for_cn.append(num_dict[str(i)])

    return str(''.join(num_for_cn))


def cn_num(c):
    cn_dict = {
        '零': '0',
        '一': '1',
        '二': '2',
        '三': '3',
        '四': '4',
        '五': '5',
        '六': '6',
        '七': '7',
        '八': '8',
        '九': '9'
    }

    cn_for_num = []
    for i in str(c):
        if i in cn_dict.keys():
            cn_for_num.append(cn_dict[str(i)])

    return str(''.join(cn_for_num))


if __name__ == '__main__':
    pass
