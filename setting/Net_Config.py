# 远程服务器连接配置
# 如果目标是Linux系统，注意修改一下
# /etc/ssh/sshd_config中的MaxSessions (指定每个网络连接允许的最大打开会话数，默认设置为10)
host = '47.97.203.200'
port = 22
user = 'root'
pwd = 'ZZGzzg666'
serverpath = '/root'    # 上传路径

# 自动化传输，默认为1分钟触发一次,单位为秒
transmit_time = 3
