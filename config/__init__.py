# -*- coding: utf-8 -*-
# @Time    : 2019/6/26 10:00 AM
# @Author  : yangmingxing
# @File    : __init__.py.py
# @Software: PyCharm
import os

def load_config():
    """
    Load a config class
    """

    mode = os.environ.get('MODE', 'DEV')
    try:
        if mode == 'PRO':
            from .pro_config import ProConfig
            return ProConfig
        elif mode == 'DEV':
            from .dev_config import DevConfig
            return DevConfig
        else:
            from .dev_config import DevConfig
            return DevConfig
    except ImportError:
        from .config import Config
        return Config


CONFIG = load_config()