#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@File    :   demo.py
@Time    :   2023/11/14 16:47:41
@Author  :   Tomoya Liu
@Version :   1.0
@Site    :   https://www.lvbibir.cn
@Desc    :   None
'''


import json

json_data = '''
{
    "data": [
        {
            "{#FSNAME}": "/",
            "{#FSTYPE}": "rootfs"
        },
        {
            "{#FSNAME}": "/sys",
            "{#FSTYPE}": "sysfs"
        },
        {
            "{#FSNAME}": "/proc",
            "{#FSTYPE}": "proc"
        },
        {
            "{#FSNAME}": "/dev",
            "{#FSTYPE}": "devtmpfs"
        },
        {
            "{#FSNAME}": "/sys/kernel/security",
            "{#FSTYPE}": "securityfs"
        },
        {
            "{#FSNAME}": "/dev/shm",
            "{#FSTYPE}": "tmpfs"
        },
        {
            "{#FSNAME}": "/dev/pts",
            "{#FSTYPE}": "devpts"
        },
        {
            "{#FSNAME}": "/run",
            "{#FSTYPE}": "tmpfs"
        },
        {
            "{#FSNAME}": "/sys/fs/cgroup",
            "{#FSTYPE}": "tmpfs"
        },
        {
            "{#FSNAME}": "/sys/fs/cgroup/systemd",
            "{#FSTYPE}": "cgroup"
        },
        {
            "{#FSNAME}": "/sys/fs/pstore",
            "{#FSTYPE}": "pstore"
        },
        {
            "{#FSNAME}": "/sys/fs/cgroup/cpu,cpuacct",
            "{#FSTYPE}": "cgroup"
        },
        {
            "{#FSNAME}": "/sys/fs/cgroup/cpuset",
            "{#FSTYPE}": "cgroup"
        },
        {
            "{#FSNAME}": "/sys/fs/cgroup/hugetlb",
            "{#FSTYPE}": "cgroup"
        },
        {
            "{#FSNAME}": "/sys/fs/cgroup/perf_event",
            "{#FSTYPE}": "cgroup"
        },
        {
            "{#FSNAME}": "/sys/fs/cgroup/memory",
            "{#FSTYPE}": "cgroup"
        },
        {
            "{#FSNAME}": "/sys/fs/cgroup/pids",
            "{#FSTYPE}": "cgroup"
        },
        {
            "{#FSNAME}": "/sys/fs/cgroup/devices",
            "{#FSTYPE}": "cgroup"
        },
        {
            "{#FSNAME}": "/sys/fs/cgroup/blkio",
            "{#FSTYPE}": "cgroup"
        },
        {
            "{#FSNAME}": "/sys/fs/cgroup/net_cls,net_prio",
            "{#FSTYPE}": "cgroup"
        },
        {
            "{#FSNAME}": "/sys/fs/cgroup/freezer",
            "{#FSTYPE}": "cgroup"
        },
        {
            "{#FSNAME}": "/sys/kernel/config",
            "{#FSTYPE}": "configfs"
        },
        {
            "{#FSNAME}": "/",
            "{#FSTYPE}": "xfs"
        },
        {
            "{#FSNAME}": "/proc/sys/fs/binfmt_misc",
            "{#FSTYPE}": "autofs"
        },
        {
            "{#FSNAME}": "/dev/mqueue",
            "{#FSTYPE}": "mqueue"
        },
        {
            "{#FSNAME}": "/sys/kernel/debug",
            "{#FSTYPE}": "debugfs"
        },
        {
            "{#FSNAME}": "/dev/hugepages",
            "{#FSTYPE}": "hugetlbfs"
        },
        {
            "{#FSNAME}": "/boot",
            "{#FSTYPE}": "xfs"
        },
        {
            "{#FSNAME}": "/var",
            "{#FSTYPE}": "xfs"
        },
        {
            "{#FSNAME}": "/opt",
            "{#FSTYPE}": "xfs"
        },
        {
            "{#FSNAME}": "/var/lib/nfs/rpc_pipefs",
            "{#FSTYPE}": "rpc_pipefs"
        },
        {
            "{#FSNAME}": "/run/user/1000",
            "{#FSTYPE}": "tmpfs"
        },
        {
            "{#FSNAME}": "/proc/sys/fs/binfmt_misc",
            "{#FSTYPE}": "binfmt_misc"
        },
        {
            "{#FSNAME}": "/sys/fs/fuse/connections",
            "{#FSTYPE}": "fusectl"
        },
        {
            "{#FSNAME}": "/proc/fs/nfsd",
            "{#FSTYPE}": "nfsd"
        },
        {
            "{#FSNAME}": "/data",
            "{#FSTYPE}": "ext4"
        },
        {
            "{#FSNAME}": "/data1",
            "{#FSTYPE}": "ext4"
        },
        {
            "{#FSNAME}": "/run/user/42",
            "{#FSTYPE}": "tmpfs"
        }
    ]
}
'''

data_dict = json.loads(json_data)

filtered_items = [item for item in data_dict['data'] if item['{#FSTYPE}'] in ['ext4', 'xfs']]

for item in filtered_items:
    print(item.get('{#FSNAME}'))

