#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2024/07/31 10:56:03
@Author  :   Liu
@Version :   1.0
@Site    :   https://www.lvbibir.cn
@Desc    :   None
'''

import re
import os
import sys
import ipaddress

if getattr(sys, "frozen", False):
    PWD = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    PWD = os.path.dirname(os.path.abspath(__file__))

def is_valid_ip(ip):
    # 使用正则表达式确认 ip 地址是否合法
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip) is not None

# 定义一个函数来获取 IP 地址的网段
def get_network(ip):
    return str(ipaddress.ip_network(ip, strict=False))

def check_ip_file(ip_file):
    with open(ip_file, 'r', encoding='utf-8') as file:
        for line in file:
            ip = line.strip()
            if not is_valid_ip(ip):
                print(f"not valid ipaddress: {ip}")

def get_ip_net_dict(ip_file, net_file):
    net_dict = {}

    with open(ip_file, encoding="utf-8") as file:
        for ip in file:
            ip = ip.split()[0]
            net = get_network(ip)
            if net in net_dict:
                net_dict[net] += 1
            else:
                net_dict[net] = 1

    with open(net_file, 'w', encoding="utf-8") as file:
        for key, value in net_dict.items():
            file.write(f"{key}, {value}\n")

if __name__ == "__main__":
    ip_file = f"{PWD}/ip_addresses.txt"
    net_file = f"{PWD}/ip_net.csv"
    # check_ip_file(ip_file)
    get_ip_net_dict(ip_file, net_file)