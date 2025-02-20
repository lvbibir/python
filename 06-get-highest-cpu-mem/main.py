#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    :   main.py
@Time    :   2023/08/14 23:34:35
@Author  :   Tomoya Liu
@Version :   1.0
@Site    :   https://www.lvbibir.cn
@Desc    :   None
"""

import os
import sys
import pandas as pd

# 获取当前 python 所在的文件夹的绝对路径
# 如果是 python 解释器, PWD 为 py 文件的目录名
# 如果是二进制程序, PWD 为 二进制程序的目录名
if getattr(sys, "frozen", False):
    PWD = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    PWD = os.path.dirname(os.path.abspath(__file__))

# 原始数据的存放目录
DIRECTORY = '/mnt/c/Users/lvbibir/OneDrive/4-管道局/2-日常工作/2023-09-27 ECS 性能报表整合/统一客服ECS性能报表0912-0926'


def list_files_in_directory(directory: str) -> list:
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('xlsx'):
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list


def find_dicts_by_key_value(dict_list: list, key: str, value: str) -> dict:
    """
    提供一个字典列表 [{}, {}, {}], 根据指定 key 的 value 输出字典

    :param list dict_list:
    :param str  key:
    :param str  value:
    """
    return [d for d in dict_list if d.get(key) == value]


def main():
    # 获取要读取的所有文件名称
    file_list = list_files_in_directory(DIRECTORY)

    # 使用第一个文件初始化 finally_list
    finally_list = []
    init_info = pd.read_excel(sheet_name="表格", io=file_list[0]).to_dict("records")
    for server_info in init_info:
        server_info_dict = {
            # "区域": server_info["区域"],
            "VDC名称": server_info["VDC名称"],
            "名称": server_info["名称"],
            "CPU使用率峰值 %": server_info["CPU使用率峰值（%）"],
            "内存使用率峰值 %": server_info["内存使用率峰值（%）"],
            "CPU取值文件": os.path.basename(file_list[0]),
            "内存取值文件": os.path.basename(file_list[0]),
        }
        finally_list.append(server_info_dict)

    # 获取每天的服务器信息
    servers_info_allday = []
    for file in file_list:
        # 将每天的数据统一到 servers_info_allday 字典中
        servers_info_oneday = pd.read_excel(sheet_name="表格", io=file).to_dict("records")
        for num in range(len(servers_info_oneday)):
            servers_info_oneday[num]["CPU取值文件"] = os.path.basename(file)
            servers_info_oneday[num]["内存取值文件"] = os.path.basename(file)
        servers_info_allday += servers_info_oneday

    # for i in find_dicts_by_key_value(servers_info_allday, "名称", "JL-ZNFW-AI-0001"):
    #     print(i)
    # return

    # 更新 finally_list
    for i in range(len(finally_list)):
        single_server_info = finally_list[i]
        name = single_server_info["名称"]
        for item in find_dicts_by_key_value(
            dict_list=servers_info_allday, key="名称", value=name
        ):
            try:
                if float(item["CPU使用率峰值（%）"]) > float(single_server_info["CPU使用率峰值 %"]):
                    finally_list[i]["CPU使用率峰值 %"] = float(item["CPU使用率峰值（%）"])
                    finally_list[i]["CPU取值文件"] = item["CPU取值文件"]
            except ValueError:
                pass

            try:
                if float(item["内存使用率峰值（%）"]) > float(single_server_info["内存使用率峰值 %"]):
                    finally_list[i]["内存使用率峰值 %"] = float(item["内存使用率峰值（%）"])
                    finally_list[i]["内存取值文件"] = item["内存取值文件"]
            except ValueError:
                pass

    # 将结果写入 csv 文件
    df = pd.DataFrame(finally_list)
    csv_file_path = DIRECTORY + "/result.csv"
    df.to_csv(csv_file_path, index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    main()
    # print(list_files_in_directory(DIRECTORY))
