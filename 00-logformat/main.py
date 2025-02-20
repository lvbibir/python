#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   logformat.py
@Time    :   2023/03/22 16:32:12
@Author  :   Levi Liu
@Version :   1.0
@Site    :   https://www.lvbibir.cn
@Desc    :   None
"""

import logging


def create_log(name="root", filename="test.log", level=10, fh_level=10, sh_level=10):
    """
    DEBUG=10 INFO=20 WARNING=30 ERROR=40 CRITICAL=50
    :param name:      日志收集器名字,默认root
    :param filename:  日志文件的名称,默认test.log
    :param level:     日志收集器的等级,默认10
    :param fh_level:  日志文件输出日志的等级,默认10,设置为0关闭文件输出
    :param sh_level:  控制台输出日志的等级,默认10,设置为0关闭终端输出
    """

    # 创建日志收集器
    log = logging.getLogger(name)

    # 输出格式
    formats = (
        "%(asctime)s - [%(funcName)s-->line:%(lineno)d] - %(levelname)s: \t %(message)s"
    )
    log_format = logging.Formatter(fmt=formats)

    # 创建日志收集器的等级
    log.setLevel(level=level)

    # 日志文件输出
    if fh_level:
        fh = logging.FileHandler(filename=filename, encoding="utf-8")
        fh.setLevel(level=fh_level)
        fh.setFormatter(log_format)
        log.addHandler(fh)

    # 终端输出
    if sh_level:
        sh = logging.StreamHandler()
        sh.setLevel(level=sh_level)
        sh.setFormatter(log_format)
        log.addHandler(sh)

    return log


if __name__ == "__main__":
    log = create_log(
        name="rose_log",
        level=10,
        filename="test.log",
        fh_level=10,
        sh_level=10,
    )
    log.debug(msg="--------debug--------")
    log.info(msg="--------info--------")
    log.warning(msg="--------warning--------")
    log.error(msg="--------error--------")
    log.critical(msg="-------critical------")
