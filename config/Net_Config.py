# 远程服务器连接配置
# 如果目标是Linux系统，注意修改一下
# /etc/ssh/sshd_config中的MaxSessions (指定每个网络连接允许的最大打开会话数，默认设置为10)
host = '192.168.1.106'
# host = '192.168.31.168'

port = 22
username = 'root'
password = '666666'
serverpath = '/home/test/'  # 上传路径
down_path = None  # 下载路径
# 自动化传输，默认为1分钟触发一次,单位为秒
transmit_time = 3

# s_host = '127.0.0.1'
# c_host = '127.0.0.1'
# post = 8090
# bsize = 10*1024*1024

update_adress = ''
