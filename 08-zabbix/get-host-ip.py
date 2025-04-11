#!/usr/bin/python3
# coding=utf-8

# https://www.zabbix.com/documentation/3.4/en/manual/api/reference/alert/get

# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI

# zabbix地址和登录信息
# ZABBIX_SERVER = 'http://11.54.90.29:10001/zabbix'
ZABBIX_SERVER = 'http://10.29.222.29:10001/zabbix'
zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login('Admin', 'zyzxykf@2021')

result_total = 0
result_used = 0

# 获取 host 列表
host_list = zapi.host.get(
    output=["hostid", "name"],
    selectInterfaces=["ip"],
)

host_ip_list = []

for host in host_list:
    host_ip_list.append(host["interfaces"][0]["ip"])

host_ip_list.sort()
host_count = len(host_ip_list)

print(f"主机数量{host_count}")
# 按照 ip 地址排序并输出
for host in host_ip_list:
    print(host)
