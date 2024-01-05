#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    :   main.py
@Time    :   2023/08/07 15:38:16
@Author  :   Tomoya Liu
@Version :   1.0
@Site    :   https://www.lvbibir.cn
@Desc    :   None
"""

import os
import sys
import re
import time
import argparse
import paramiko
import pandas as pd
from paramiko import Channel
from logformat import create_log

# 获取当前 python 所在的文件夹的绝对路径
# 如果是 python 解释器, PWD 为 py 文件的目录名
# 如果是二进制程序, PWD 为 二进制程序的目录名
if getattr(sys, "frozen", False):
    PWD = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    PWD = os.path.dirname(os.path.abspath(__file__))

# 参数列表
usage = """
--try       测试主机连通性
--scp       发送文件到远程主机
--run       远程执行命令
--log       日志文件存储路径
-f file     指定 csv 文件的路径
--print     解析指定的 csv 文件

csv 文件的格式如下

hostname port username password root_password new_password
1.1.1.1   22   sysadmin  xxx      xxxxx        xxxxxx
eg.com    33   normal    xxx      xxxxx        xxxxxx
"""
parser = argparse.ArgumentParser(description="manual to this script", usage=usage)
parser.add_argument("--try", type=bool, default=False)
parser.add_argument("--scp", type=bool, default=False)
parser.add_argument("--run", type=bool, default=False)
parser.add_argument("--print", type=bool, default=False)
parser.add_argument("-f", type=str, default=PWD + "server_info.csv")
parser.add_argument("--logfile", type=str, default=PWD + "batchromote.log")
args = parser.parse_args()


ssh_timeout = 10.0  # SSH 超时时间
blank_timeout = 30.0  # 允许空白无输出最长多久
isbreak = 0
recv_len = 1024 * 10
general_user_ending_char = r"\]\$ "
root_ending_char = r"\]\# "

# 日志收集器
log = create_log(
    name="batchremote",
    level=10,
    fh_level=10,
    sh_level=20,
    filename=(PWD + "/batchremote.log"),
)


help_info = """
usage :

--try       测试主机连通性
--scp       发送文件到远程主机
--run       远程执行命令
--log       日志文件存储路径
-f file     指定 csv 文件的路径
--print     解析指定的 csv 文件

csv 文件的格式如下

hostname port username password root_password new_password
1.1.1.1   22   sysadmin  xxx      xxxxx        xxxxxx
eg.com    33   normal    xxx      xxxxx        xxxxxx
"""


class PtySession(object):
    def __init__(self, session: Channel, ending_char: str, timeout: float = 30.0):
        """
        交互式执行远程命令

        :param str   ending_char:
            单次命令以及销毁 session 的结束符
        :param float timeout:
            没有任何输入输出一定时间后视为超时
        """
        super().__init__()
        self.session = session  # type:Channel
        self.last_line = ""
        self.ending_char = ending_char  # send 方法执行的结束符
        self.timeout = timeout  # 没有输入也没有输出时的超时时间
        self.clear_tail()

    def clear_tail(self):
        """
        清理输出还处于缓冲区中未读取的流, 未匹配到定界符时按照 self.timeout 配置强制关闭
        """
        wait_time = 0.0
        while True:
            time.sleep(0.2)
            # self.session.recv_ready()在读取过程中不一定总是True，只有当读取缓冲流中有字节读取时，才会为True。所以在读取头一次后获取下次流到缓冲区中前为False
            if self.session.recv_ready():
                self.last_line = self.session.recv(recv_len).decode("utf-8")
                log.info(msg=f"return:\n{self.last_line}")
            if re.search(self.ending_char, self.last_line):
                break
            wait_time += 0.2
            if wait_time > self.timeout:
                global isbreak
                isbreak = 1
                break

    def destroy(self):
        """
        销毁并关闭 session
        """
        self.clear_tail()
        self.session.close()

    def exp(self, *exp_cmds: tuple):
        """
        期望并执行，与expect的用法类似。
        第一个元素为获取的期望结束字符，第二个元素为需要执行的命令，如果传入的第三个元素，则第三个元素必须为元组，并且也同父级一样，属递归结构。
        :param tuple exp_cmds:
        """
        interval = 0.2
        cur_time = 0.0
        while True:
            if self.session.recv_ready():
                self.last_line = self.session.recv(recv_len).decode("utf-8")
                log.info(msg=f"return:\n{self.last_line}")
            elif self.session.send_ready():
                for exp_cmd in exp_cmds:
                    _cmd = exp_cmd[1]
                    if not _cmd.endswith("\r"):
                        _cmd += "\r"
                    match = re.search(exp_cmd[0], self.last_line)
                    print(exp_cmd[0])
                    if match and match.group():
                        log.info(msg=f"send: {_cmd}")
                        self.session.send(_cmd)
                        # 清空最后一行数据缓存，便于下个命令的读取流输出。此行代码去除，会导致无法等待命令执行完毕提前执行后续代码的问题。
                        self.last_line = ""
                        if len(exp_cmd) == 3 and exp_cmd[2]:
                            self.exp(exp_cmd[2])
                        return
            # 如果既没有输出也没有输入, 则等待 self.timeout 关闭连接
            cur_time += interval
            if cur_time >= self.timeout:
                raise Exception("timeout...")
            time.sleep(interval)

    def send(self, cmd: str):
        """
        单纯的发送命令到目标服务器执行。
        :param str cmd:
        """
        self.last_line = ""
        if not cmd.endswith("\r"):
            cmd += "\r"
        log.info(msg=f"send commad: {cmd}")
        self.session.send(cmd)
        self.clear_tail()


def try_connect(server: dict, timeout: float = 10.0):
    """
    测试 ssh 连接

    :param dict  server:
        server 字典必须字段: hostname, port, username, password
    :param float timeout:
        ssh 连接超时时间
    """
    _ssh_client = paramiko.SSHClient()
    _ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    _ssh_client.set_log_channel(name=log.name)
    try:
        _ssh_client.connect(
            hostname=server["hostname"],
            port=server["port"],
            username=server["username"],
            password=server["password"],
            timeout=timeout,
        )
        log.info(msg=f"{server['hostname']} 测试连接成功")
    except Exception as e3:
        log.error(msg=f"{server['hostname']} 测试连接失败: {e3}")
    _ssh_client.close()


def upload_files(server: dict, files: dict):
    """
    上传文件至服务器

    :param dict server:
        server 字典必须字段 hostname, port, username, password
    :param dict files:
        上传的文件列表, 列表中的每个元素应为字典

        {"localpath": "current_localpath", "remotepath": "current_remotepath"}

        localpath 和 remotepath 必须精确到文件名
    """
    _tran = paramiko.Transport((server["hostname"], server["port"]))
    _tran.set_log_channel(log.name)
    _tran.connect(username=server["username"], password=server["password"])

    try:
        _sftp_client = paramiko.SFTPClient.from_transport(_tran)
        log.info(msg=f"{server['hostname']} sftp 连接成功.")
    except Exception as e1:
        log.error(msg=f"{server['hostname']} sftp 连接失败:{e1}")
        return False
    for file in files:
        try:
            _sftp_client.put(file["localpath"], file["remotepath"])
            log.info(msg=f"{server['hostname']} {file['remotepath']} 文件上传成功.")
        except Exception as e2:
            log.error(msg=f"{server['hostname']} {file['remotepath']} 文件上传失败:\n{e2}")
    _sftp_client.close()


def run_commands(server: dict, commands: list, ending_char: str) -> None:
    """
    连接服务器并执行命令

    :param dict  server:
        server 字典必须字段: hostname, port, username, password
    :param str ending_char:
        当终端出现指定字符串时视为命令执行结束, `单次命令`以及`所有命令结束`时使用
    :param list commands:
        需要执行的命令列表, 命令分为`单次命令`和`交互式命令`
        - 单次命令: 类似登录后直接退出
        - 交互式命令: 登录后根据命令中指定的 `第一个` 元素作为提示符进行操作, 支持递归写法

            示例:

            ```text
            (
                r"\]\$ ",        # 这里表示普通用户登录成功, 普通用户 PS1 的默认提示符, 也可以使用用户名等信息
                "run_a_command", # 相当于键盘输入命令后回车
                (
                    "(yes|no)",  # 上条命令执行结果中出现该字符串时
                    "yes",       # 输入 yes
                    (
                        "are u sure?", # 又一条提示
                        "",            # 空字符串表示直接回车
                    ),
                ),
            ),
            ```
    """
    _ssh_client = paramiko.SSHClient()
    _ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    _ssh_client.set_log_channel(name=log.name)
    try:
        _ssh_client.connect(
            hostname=server["hostname"],
            port=server["port"],
            username=server["username"],
            password=server["password"],
            timeout=ssh_timeout,
        )
        log.info(msg=f"{server['hostname']} ssh 连接成功.")
    except Exception as e3:
        log.error(msg=f"{server['hostname']} ssh 连接失败: {e3}")

    _ssh_session = _ssh_client.get_transport().open_session(
        timeout=1 * 3600
    )  # type:Channel
    _ssh_session.get_pty()
    _ssh_session.invoke_shell()

    pty_session = PtySession(
        _ssh_session, ending_char=ending_char, timeout=blank_timeout
    )

    # isbreak 变量用于控制当某条指令超时或者错误时结束后续所有命令流
    global isbreak

    for command in commands:
        if isbreak:
            break
        if isinstance(command, str):
            pty_session.send(command)
        elif isinstance(command, tuple):
            pty_session.exp(command)
        else:
            log.error(msg="传入参数错误, 期望 str or tuple")

    if isbreak:
        log.error(msg=f"{blank_timeout} 秒内没有定界符输出, 停止该主机的后续命令执行")
        pty_session.session.close()
        return False

    pty_session.destroy()


def main():
    server_info_csv = PWD + "/server_info.csv"
    if not os.path.exists(server_info_csv):
        print(help_info)
        return
    # 获取服务连接信息，字典格式
    df = pd.read_csv(server_info_csv)
    servers = df.to_dict("records")

    if len(sys.argv) != 2:
        print(help_info)
    # 测试连接
    elif sys.argv[1] == "try":
        for server in servers:
            try_connect(server, ssh_timeout)
    # 上传文件
    elif sys.argv[1] == "scp":
        # 文件需要一一对应
        files = [
            {"localpath": PWD + "/files/test.txt", "remotepath": "/tmp/test.txt"}
            # {"localpath": "localpath_2", "remotepath": "remotepath_2"},
            # {"localpath": "localpath_3", "remotepath": "remotepath_3"},
        ]
        for server in servers:
            upload_files(server, files)
            log.info(msg=f"{server['hostname']} 任务执行完毕")
    # 执行命令
    elif sys.argv[1] == "run":
        for server in servers:
            commands = [
                (
                    root_ending_char,
                    "passwd root",
                    (
                        "New password",
                        f"{server['new_passwd']}",
                        ("Retype new password", f"{server['new_passwd']}"),
                    ),
                ),
            ]
            if server["username"] == "root":
                ending_char = root_ending_char
            else:
                ending_char = general_user_ending_char
                command_su_root = [
                    (
                        ending_char,
                        "su root",
                        ("Password", f"{server['root_password']}"),
                    ),
                ]
                command_su_back = [
                    f"su {server['username']}",
                ]
                commands = command_su_root + commands + command_su_back

            run_commands(server, commands, ending_char=ending_char)
            log.info(msg=f"{server['hostname']} 任务执行完毕")
    else:
        print(help_info)


if __name__ == "__main__":
    main()

