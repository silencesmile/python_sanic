# -*- coding: utf-8 -*-
# @Time    : 2019/6/26 10:00 AM
# @Author  : yangmingxing
# @File    : dev_config.py
# @Software: PyCharm

'''
开发环境配置项

'''
from .config import Config


class DevConfig(Config):
    """
    Dev config for demo02
    """

    # Application config
    DEBUG = True

    # mysql设置
    MYSQL_HOST = "127.0.0.1"
    MYSQL_POST = 3306
    MYSQL_USER = "root"
    MYSQL_PASS = ""
    MYSQL_DB = "voice_db"

    # redis设置
    REDIS_HOST = "127.0.0.1"
    REDIS_POST = 6379
    REDIS_PASS = ""
    SELECT_DB = 2

    REQUEST_MAX_SIZE = 1000000

'''
框架默认的项目配置参数：

名称	                              默认值	                   描述
REQUEST_MAX_SIZE	           100000000         	请求报文的字节数
REQUEST_BUFFER_QUEUE_SIZE	      100	            请求流的缓存队列限制
REQUEST_TIMEOUT	                  60	            请求超时时间（秒）
RESPONSE_TIMEOUT	              60            	响应超时时间（秒）
KEEP_ALIVE	                    True	           设置为False时将设置短链接
KEEP_ALIVE_TIMEOUT                5	               每个TCP链接保持的时间（秒）
GRACEFUL_SHUTDOWN_TIMEOUT	     15.0	          强制关闭非空链接的时间（秒）
ACCESS_LOG	                    True	         是否开启登陆日志功能

'''