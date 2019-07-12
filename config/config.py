# -*- coding: utf-8 -*-
# @Time    : 2019/6/26 10:00 AM
# @Author  : yangmingxing
# @File    : config.py
# @Software: PyCharm

'''
共有配置项

'''

import os


class Config():
    """
    Basic config for demo02
    """
    # Application config
    TIMEZONE = 'Asia/Shanghai'
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # redis设置
    REDIS_HOST = "127.0.0.1"
    REDIS_POST = 6379
    REDIS_PASS = ""
    SELECT_DB = 2