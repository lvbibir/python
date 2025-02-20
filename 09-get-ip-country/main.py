#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    :   main.py
@Time    :   2024/07/24 09:45:28
@Author  :   Tomoya Liu
@Version :   1.0
@Site    :   https://www.lvbibir.cn
@Desc    :   None
"""

import os
import re
import sys
import time
import requests
from tqdm import tqdm

if getattr(sys, "frozen", False):
    PWD = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    PWD = os.path.dirname(os.path.abspath(__file__))


def get_data(url):
    try:
        # 发送 GET 请求
        response = requests.get(url)

        # 检查请求是否成功 如果请求失败，会抛出异常
        response.raise_for_status()

        # 解析 JSON 数据
        json_data = response.json()
        return json_data

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None
    except ValueError as e:
        print(f"解析 JSON 时出错: {e}")
        return None


def is_valid_ip(ip):
    # 使用正则表达式确认 ip 地址是否合法
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip) is not None

def get_ip_list(ip_file_path):

    valid_ip_list = []
    not_valid_ip_list = []

    try:
        with open(ip_file_path, "r", encoding="utf-8") as file:
            for line in file:
                # 去除行首尾空白字符
                line = line.strip()
                if line: # 过滤空白行
                    # 去除可能的 '/24' 等后缀
                    ip = line.split('/')[0]
                    if is_valid_ip(ip): # 仅添加有效的 IP 地址
                        valid_ip_list.append(ip)
                    else:
                        not_valid_ip_list.append(ip)
            if len(not_valid_ip_list):
                print(f"{ip_file_path} has not valid ip:")
                for ip in not_valid_ip_list:
                    print(ip) 
                return []
        return valid_ip_list
    except FileNotFoundError:
        print(f"文件未找到: {ip_file_path}")
        return []
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return []


if __name__ == "__main__":
    # url = "https://qifu-api.baidubce.com/ip/geo/v1/district?ip=185.224.128.47"
    result_file_path = PWD + "/" + "result.csv"
    ip_file_path = PWD + "/" + "ip.txt"
    ip_list = get_ip_list(ip_file_path)

    if len(ip_list):
        with open(result_file_path, "w", encoding="utf-8-sig") as file:
            for ip in tqdm(ip_list, desc="processing Items"):
                time.sleep(0.5)
                url = f"https://qifu-api.baidubce.com/ip/geo/v1/district?ip={ip}"
                data = get_data(url)
                if data is not None:
                    result = f"{ip},{data['code']},{data['data']['country']},{data['data']['prov']},{data['data']['city']}"
                    file.write(result + "\n")
