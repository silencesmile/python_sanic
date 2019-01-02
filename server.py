# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 5:31 PM
# @Author  : 大杨子Young
# @File    : server.py
# @Software: PyCharm

#@公众号：python疯子

import pymysql
import redis
import json as python_json
import logging

from sanic import Sanic
from sanic import response
from sanic.response import text
from sanic.response import json
from sanic.config import Config
from sanic.exceptions import RequestTimeout
from cacheout import CacheManager, LRUCache
from twisted.internet import threads, reactor

from set_config import *
from voice_app.wavTools import *


# 异步子线程开开启的线程数
reactor.suggestThreadPoolSize(1)

logger = logging.getLogger(__name__)

# 继承类的目的：启动服务时预加载数据 和 添加缓存功能
# 方法很笨，如有好的方法请建议
class Sanic_server(Sanic):

    def __init__(self):
        # 重写并继承父类的init方法
        super(Sanic_server, self).__init__()

        self.dict = {}
        self.redis_obj = self._create_redis_connection_pool(REDIS_HOST, REDIS_POST, REDIS_PASS, SELECT_DB)

        '''
        当你经常使用某些数据模板和信息时就要考虑缓存了
        缓存机制：cacheout
        设置多个缓存， 并设置缓存机制
        maxsize：代码缓存保留信息条目数
        ttl：每条信息的有效期（单位：秒）
        LRU (最近最少使用机制)，就是删除最近最少使用的，保留最近最多使用的
        具体介绍：公众号-python疯子
        
        '''
        self.cache = CacheManager({"voice_store": {"maxsize": 1000},
                                    "mysql_store": {"maxsize": 1000, "ttl": 2529000}},
                                  cache_class=LRUCache)


    @staticmethod
    def _create_redis_connection_pool(ip, port, password, db):
        """创建redis连接池"""

        pool = redis.ConnectionPool(host=ip, port=int(port), password=password, db=db)
        redis_tool = redis.Redis(connection_pool=pool)
        return redis_tool

Config.REQUEST_TIMEOUT = 3
app = Sanic_server()

@app.route("/voice_server/v1", methods=["POST"])
async def func(request):
    '''
    流程：下载音频，读取音频信息并返回

    :param request: 包含音频名称的URL， 此处只为音频名称
    :return:  音频信息
    '''

    # 通过模板向数据库请求url信息
    voice = request.json
    template = voice.get("template")

    # 先判断内存中
    boolen = app.cache["mysql_store"].has(template)
    if boolen:
        voice_info = app.cache["mysql_store"].get(template)
    else:
        voice_info = start_new_scene(template)

    # 'http://www.python_sanic.com/demo.wav'
    voice_url = voice_info[2]

    # 因为音频网址为假的，所以下载就略过
    voice_id = voice_url.split("/")[-1]
    voice_path = "voice_app/voice_files/" + voice_id

    # 记录用户请求信息
    # 存在redis中，因为如果以后做负载均衡，可能不在通过一个服务上，用redis就能保证统一性
    # 存储用户请求信息
    threads.deferToThread(save_user_info, "voice_body", voice, 1)

    # 判断缓存中是否包含次音频信息，
    # 如果存在直接获取，如果不存在，在先获取，再返回，然后异步存储
    boolen = app.cache["voice_store"].has(voice_id)
    if boolen:
        voice_body = app.cache["voice_store"].get(voice_id)
    else:
        # 获取音频内容
        voice_body = read_wav(voice_path)

        # 子线程异步音频信息
        threads.deferToThread(save_voice_body, voice_id, voice_body)

    return text(voice_body)


@app.route('/voice_server/<voice_id>', methods=['GET'])
async def person_handler(request, name):

    try:
        voice = request.json
        voice_id = voice.get("voice")
        voice_path = "voice_app/voice_files/" + voice_id

        voice_time = get_wav_time(voice_path)

        response_dict = {
            "error":0,
            "err_msg":"",
            "voice_time": voice_time
            }

        voice_json = python_json.dumps(response_dict)

        return voice_json
    except Exception as e:
        logger.error(e)
        response_dict = {
                        "error": 1,
                        "err_msg": "请求错误"
                        }

        voice_json = python_json.dumps(response_dict)

        return voice_json

def start_new_scene(template):
    """从数据库里读取一个scene的数据（话术模板）"""

    db = pymysql.connect(host = MYSQL_HOST, port = MYSQL_POST, user = MYSQL_USER, password = MYSQL_PASS, db = MYSQL_DB)
    cursor = db.cursor()

    sql = "SELECT * FROM `voiceInfo` where template='{}'".format(template)

    try:
        cursor.execute(sql)
        results = cursor.fetchall()[0]

        # 存储模板信息
        app.cache["mysql_store"].set(template, results)

        return results
    except:

        return False
    finally:
        db.close()

# 存储mysql模板信息
def save_template_info(template_code, template_info):
    app.cache["mysql_store"].set(template_code, template_info)


# 缓存音频信息
def save_voice_body(voice_store_key, voice_body):

    app.cache["voice_store"].set(voice_store_key, voice_body)

def save_user_info(request_info ,voice, first = None):
    user_id = voice.get("user_id")

    # 如果你的请求是有顺序的，那么就能确定第一次请求redis中必然没有， 所以可以直接存储
    if first:
        voice_info = {request_info: voice}

        app.redis_obj.setex(user_id, voice_info, 6000)
    else:
        voice_info = app.redis_obj.get(user_id)

        voice_info[request_info] = voice
        app.redis_obj.setex(user_id, voice_info, 6000)

# 防止等待超时 服务器崩溃
@app.exception(RequestTimeout)
def timeout(request, exception):
    return response.text('RequestTimeout from error_handler.', 408)


if __name__ == '__main__':
    # work 接口监听者   和内核合数相同
    app.run(host="0.0.0.0", port=8000, workers=2, debug=True)