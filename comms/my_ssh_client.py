import sys
import time

import paramiko
from comms.log_utils import get_logger


class MySshClient:
    def __init__(self, host, port, username, passwd):
        # 创建链接
        try:
            ssh = paramiko.SSHClient()  # 创建链接对象
            ssh.set_missing_host_key_policy(paramiko.WarningPolicy())  # 选择链接方式
            ssh.load_system_host_keys()
            ssh.connect(host, port, username, passwd, timeout=5)  # 输入链接信息进行链接
            self.ssh = ssh
        except Exception as e:
            print(f"链接服务器{host}:{port}失败")
            get_logger().error(f"链接服务器{host}:{port}失败")
            raise e

    # 执行shell命令
    def exec_command(self, shell):
        try:
            log = self.ssh.exec_command(shell, get_pty=True)

            return log
        except Exception as e:
            print(f"执行shell命令:{shell}失败")
            get_logger().error(f"执行shell命令:{shell}失败")
            raise e

    # 上传文件
    def put_file(self, localpath, remotepath):
        try:
            sftp = self.ssh.open_sftp()
            sftp.put(localpath, remotepath)
        except Exception as e:
            print(f"上传文件:{localpath}失败")
            get_logger().error(f"上传文件:{localpath}失败")
            raise e

    # 下载文件
    def get_file(self, remotepath, localpath):
        try:
            sftp = self.ssh.open_sftp()
            sftp.get(remotepath, localpath)
        except Exception as e:
            print(f"下载文件:{remotepath}失败")
            get_logger().error(f"下载文件:{remotepath}失败")
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ssh.close()


if __name__ == '__main__':
    # host = "192.168.25.128"
    host = '61.172.179.73'
    # port = 22
    port = 41098
    username = 'ubuntu'
    pw = "123456"
    mc = MySshClient(host, port, username, pw)
    # a = mc.exec_command('ls')
    # time.sleep(3)
    a = mc.exec_command('pwd')
    a2, b2, c2 = a
    print(b2.read().decode(), c2.read().decode())
    # time.sleep(5)
    # b = mc.exec_command('pwd')
    # a1, b1, c1 = b
    # # print(a1.read().decode())
    # print(b1.read().decode())
    # print(c1.read().decode())
