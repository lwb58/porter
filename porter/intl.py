import os
import json
import datetime
from intl import api
from movpy.api import dub
from porter import intl_redis, settings


def fetch_today_news(limit=None):
    date = str(datetime.datetime.now().date())
    for i in api.fetch_jingji_news(date, limit=limit):
        if not intl_redis.hexists("jingji_set", i["url"]):
            print(i)
            intl_redis.hset("jingji_set", i["url"], json.dumps(i))
            intl_redis.lpush("jingji_list", i["url"])


def gen_news_video():
    url = intl_redis.rpop("jingji_list")
    if url:
        data = intl_redis.hget("jingji_set", url)
        data = json.loads(data)
        filepath = os.path.join(settings.UPLOAD_PATH, data["title"] + ".mp4")
        dub(settings.DUB_VIDEO, data["content"], "yanlijie",
            filepath, speed=3, bgm=settings.DUB_BGM)
        return filepath
