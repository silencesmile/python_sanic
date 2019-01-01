# -*- coding: utf-8 -*-
# @Time    : 2019/1/1 15:31 PM
# @Author  : 大杨子Young
# @File    : server.py
# @Software: PyCharm

#@公众号：python疯子

import time

from twisted.internet import threads, reactor
from twisted.internet.defer import inlineCallbacks

# 异步子线程开开启的线程数 默认10
reactor.suggestThreadPoolSize(5)

'''
使同步函数秒变异步并发函数
如果需要返回值， 如run2()函数
给请求函数添加装饰器@inlineCallbacks
并使用yield进行接收返回值

如果不需要返回值可以使用addCallback回调函数 如run()函数
'''


def largeFibonnaciNumber():
    """
    耗时的事
    """
    TARGET = 10000

    first = 0
    second = 1

    for i in range(TARGET - 1):
        new = first + second
        first = second
        second = new
    time.sleep(3)
    return second

def fibonacciCallback(result):
    """
    回调函数
    打印耗时函数的返回结果
    """
    print ("largeFibonnaciNumber result =", result)

def run():
    """
    主函数
    """
    # 将耗时函数放入另一个线程执行，返回一个deferred对象
    d = threads.deferToThread(largeFibonnaciNumber)
    # 添加回调函数
    d.addCallback(fibonacciCallback)

    print ("1st line after the addition of the callback")
    print ("2nd line after the addition of the callback")


@inlineCallbacks
def run2():
    """
    主函数
    """
    # 将耗时函数放入另一个线程执行，返回一个deferred对象
    d = yield (threads.deferToThread(largeFibonnaciNumber))

    # 等待返回的结果 再做处理
    print(d)
    print ("1st line after the addition of the callback")
    print ("2nd line after the addition of the callback")

if __name__ == '__main__':

    for i in range(100):
        run()
    reactor.run()