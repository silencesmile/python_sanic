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