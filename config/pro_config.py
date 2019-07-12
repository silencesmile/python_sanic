# -*- coding: utf-8 -*-
# @Time    : 2019/6/26 10:01 AM
# @Author  : yangmingxing
# @File    : pro_config.py
# @Software: PyCharm

'''
生产环境配置项

'''

from .config import Config


class ProConfig(Config):
    """
    Pro config for demo02
    """

    # Application config
    DEBUG = False