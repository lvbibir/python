#!/usr/bin/python3
# coding=utf-8

# https://www.zabbix.com/documentation/3.4/en/manual/api/reference/alert/get

# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI
import re
import time

# zabbix地址和登录信息
ZABBIX_SERVER = 'http://11.54.90.29:10001/zabbix'
# ZABBIX_SERVER = 'http://10.29.222.29:10001/zabbix'
zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login('Admin', 'zyzxykf@2021')

result_total = 0
result_used = 0

# 获取 host 列表
host_list = zapi.host.get(
    output=["hostid"],
)

# 查询接口
def item_get(hostid, key):
    result=zapi.item.get(
        output=["lastvalue"],
        hostids=str(hostid),
        search={
            "key_": str(key)
        }
    )
    return result[0]['lastvalue']

# 获取单个服务器信息
def get_single_host(host):
    item_list=zapi.item.get(
        output=["key_"],
        hostids=host
    )

    # 初始化 item 列表
    disk_items_total = []
    disk_items_used = []
    regex_pattern_total = re.compile(r'vfs\.fs\.size\[[^\]]+,total\]')
    regex_pattern_used = re.compile(r'vfs\.fs\.size\[[^\]]+,used\]')

    for item in item_list:
        if regex_pattern_total.match(item['key_']):
            disk_items_total.append(item['key_'])
        if regex_pattern_used.match(item['key_']):
            disk_items_used.append(item['key_'])
    
    global result_total
    global result_used

    for item in disk_items_total:
        result_total += int(item_get(hostid=host, key=item))
    for item in disk_items_used:
        result_used += int(item_get(hostid=host, key=item))

def main():
    for host in host_list:
        get_single_host(host['hostid'])
        print(result_total, result_used)
        time.sleep(1)

main()