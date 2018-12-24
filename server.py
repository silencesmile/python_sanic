import pymysql
import redis

from sanic import Sanic
from sanic.response import text
from sanic.response import json

from config import *


class SanicServer(object):
    app = Sanic(__name__)

    def __init__(self):
        self.dict = {}
        self.redis_obj = self._create_redis_connection_pool(REDIS_HOST, REDIS_POST, REDIS_PASS, SELECT_DB)

    @staticmethod
    def _create_redis_connection_pool(ip, port, password, db):
        """创建redis连接池"""

        pool = redis.ConnectionPool(host=ip, port=int(port), password=password, db=db)
        redis_tool = redis.Redis(connection_pool=pool)
        return redis_tool

    def start_new_scene(self, scene_id, version):
        """从数据库里读取一个scene的数据（话术模板）"""

        db = pymysql.connect(host = MYSQL_HOST, port = MYSQL_POST, user = MYSQL_USER, password = MYSQL_PASS, db = MYSQL_DB)
        cursor = db.cursor()

        sql = "SELECT * FROM `biz_scene` WHERE speech_id='{}' and version='{}'".format(scene_id, version)

        try:
            cursor.execute(sql)
            results = cursor.fetchall()

            # print(results)

            return results
        except:

            return False
        finally:
            db.close()

    @app.route("/")
    async def index(self, request):

        return text('Hello World!')

    @app.route('/person/<name:[A-z]+>')
    async def person_handler(self, request, name):

        print(name)

        return text('2222222')


    @app.route('/tag')
    async def tag_handler(self, request):
        for i in range(10):
            ret = self.start_new_scene("5", "1")
            print(ret)

        response = json({"hello": "world"})
        return response


if __name__ == '__main__':
    sanic = SanicServer()
    # work 接口监听者   和内核合数相同
    sanic.app.run(host="0.0.0.0", port=8000, workers=2)