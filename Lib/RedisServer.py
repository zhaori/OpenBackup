import redis


class RedisServer(object):

    def __init__(self, host, port, db=None):
        self.r = redis.StrictRedis(host=host, port=port, decode_responses=True, db=db, max_connections=15)

    def key_in_data(self, key_set) -> bool:
        """
        检查key是否是数据库里唯一存在
        return: True为存在，False 为不存在
        """
        return self.r.exists(key_set)

    def set(self, key, value, nx=None):
        """
        key: str
        return: 插入单条记录
        """
        self.r.set(key, value, nx)

    def set_all(self, value: dict):
        """
        批量插入数据
        """
        if type(value) != dict:
            raise Exception('The type only dict or json')
        else:
            return self.r.mset(value)

    def delete(self, key):
        self.r.delete(key)

    def search(self, key):
        return eval(self.r.get(key))

    def update(self, old, new):
        """
        更新单条数据,根据key更新值
        """
        self.r.getset(old, new)

    def save(self):
        """
        内存数据本地持久化
        """
        self.r.save()

    def flush(self):
        """
        清除内存数据
        """
        self.r.flushall()


if __name__ == "__main__":
    from config.redis_config import *
    r = RedisServer(redis_host, redis_port, db=0)
    data = {
        "注册账号": "666",
        "登录密码": "666666",
        "手机号": "135xxxxxxx",
        "微信号": "135xxxxxxx",
        "邮箱": "XXXXX",
        "摊位地点": " ",
        "身份信息": {
            "姓名": "皮得狠",
            "性别": "男",
            "年龄": "2100",
            "籍贯": "中华人民共和国",
            "民族": "汉",
            "身份证住址": "四川省",
            "身份证号码": "5113211xxxxxxx77100"

        }

    }

    #r.set("data", data)
    r.save()
    #dd = r.search("data")
    #for i in dd.keys():
    #    print(i)
    # print(list(data.keys())[0])
    # r.flush()
    # r.update('name', 'zg')
