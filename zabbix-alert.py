#!/usr/bin/python3
# coding=utf-8

# https://www.zabbix.com/documentation/3.4/en/manual/api/reference/alert/get

# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI
import time

# zabbix地址和登录信息
ZABBIX_SERVER = 'http://11.54.90.29:10001/zabbix'
zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login('Admin', 'zyzxykf@2021')


if '__main__' == __name__:
    # 获取告警信息
    alert_list = zapi.alert.get(
        limit=10,
        # output=[
        #     "hosts",  # 触发器id
        #     "subject",  # 触发器内容秒数
        # ],
        # filter={"value": 1},  # 过滤，此处表示启动的触发器
        sortfield="clock",  # 排序
        sortorder="DESC",  # 正排与倒排
        # min_severity=2,  # 返回指定告警级别的告警，这里是大于等于告警
        time_from=int(
            time.mktime(time.strptime("2023-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))
        ),
        time_till=int(
            time.mktime(time.strptime("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))
        ),
        skipDependent=1,  # 跳过依赖于其他问题中的触发器
        monitored=1,  # 属于受监控主机的已启用触发器，并仅包含已启用的项目
        active=1,  # 只返回属于受监控主机的启用的触发器（与上条意思差不多，至于什么区别，未测）
        # expandDescription=1,  # 在触发器的名称中展开宏
        selectHosts=['name'],  # 在结果中返回关联的主机信息（意思就是显示出那台主机告警的）
        # selectGroups=['name'],  # 在结果中返回关联的主机组信息（意思就是显示出那个主机组告警的）
        # only_true=1,  # 只返回最近处于问题状态的触发器
    )
    info = ""
    for i in alert_list:
        if not i.get('hosts') or not i['hosts']:
            continue

        host_name = i['hosts'][0].get('name', '')
        if not host_name:  # 如果 'name' 不存在，跳过当前循环
            continue

        info += f"{host_name}\t{i['subject']}\n"

    print(len(info))

    with open('zabbix-klmy.log', 'a') as file:
        file.write(info)
