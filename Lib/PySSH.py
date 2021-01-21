import paramiko

from config.Net_Config import *


class PySSH(object):
    def __init__(self):
        self.host = host
        self.port = port
        self.ssh = paramiko.SSHClient()
        # 允许连接不在~/.ssh/known_hosts文件中的主机
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.stdin = None
        self.stdout = None
        self.stderr = None

    def login(self, command):
        self.ssh.connect(hostname=self.host, port=self.port, username=username, password=password)
        self.stdin, self.stdout, self.stderr = self.ssh.exec_command(command)

        print(self.__get_value())

    def __get_value(self):
        return [str(i).rstrip("\n") for i in self.stdout.readlines()]

    def close(self):
        self.ssh.close()


class PySFTP(object):

    def __init__(self):
        transport = paramiko.Transport(host, port)
        transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(transport)

    def sftp_up(self, local_file, server_file):
        self.sftp.put(local_file, server_file)

    def sftp_down(self, server_file, local_file):  # 0为下载备份文件与 与之对应的MD5  #1为只下载文件
        self.sftp.get(server_file, local_file)

    def sftp_close(self):
        self.sftp.close()


"""
class PYSCP(object):
    def __init__(self, user=None, pwd=None, mode=None):
        if user is None:
            user = username
        if pwd is None:
            pwd = password
        self.host = host
        self.usr = user
        self.pwd = pwd
        self.hostpath = serverpath
        if mode is None:
            self.login = f"pscp -l {self.usr} -pw {str(self.pwd)} -r"
        elif mode == 1:
            self.login = f"pscp -l {self.usr} -pw {str(self.pwd)}"

    def scp_up(self, file):
      
        # print(f"{self.login} {file} {self.usr}@{self.host}:{self.hostpath}")
        os.system(f"{self.login} {file} {self.usr}@{self.host}:{self.hostpath}")

    def scp_down(self, file, local):
      
        os.system(
            f"{self.login} {self.usr}@{self.host}:{os.path.join(self.hostpath, file)} {os.path.join(local, file)}")
"""

if __name__ == '__main__':
    # for i in os.listdir(r".\Temp"):
    pass
