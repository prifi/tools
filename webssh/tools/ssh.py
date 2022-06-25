
# paramiko SSH
import paramiko
import sys

class SSHClient:
    def __init__(self, host, username, password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        try:
            client.connect(self.host, self.port, self.username, self.password)
            # 异常
            self.__sshclient = client
        except Exception as e:
            # 日志处理
            raise

    def exec(self, cmd:str):
        return self.__sshclient.exec_command(cmd)

    def close(self):
        return self.__sshclient.close()


if __name__ == '__main__':

    client = SSHClient('192.168.142.140', 'python', 'python') # ip port username, password
    print(type(client), client)
    stdin, stdout, stderr = client.exec('/usr/sbin/ip a')
    # print(stdout.read()) # makefile socket file(read write) io 一来一回
    # print(stderr.read())
    output1 = stdout.read() # utf-8
    output2 = stderr.read()
    print('=' * 30)
    print(output1.decode())
    print('-' * 30)
    if output2:
        print(output2.decode(), file=sys.stderr)
    print('=' * 30)
    client.close()
