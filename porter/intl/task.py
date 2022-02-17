import os
import json
import datetime
from intl.api import fetch_jingji_news
from movpy.api import dub
from porter import redis_client, settings


def fetch_today_news(limit=None):
    date = str(datetime.datetime.now().date())
    for i in fetch_jingji_news(date, limit=limit):
        if not redis_client.hexists("intl", i["url"]):
            print(i["title"])
            redis_client.hset("intl", i["url"], json.dumps(i))
            redis_client.lpush("intl", i["url"])


def gen_news_video():
    url = redis_client.rpop("intl")
    data = redis_client.hget("intl", url)
    data = json.loads(data)
    filepath = os.path.join(settings.UPLOAD_PATH, data["title"] + ".mp4")
    dub(settings.DUB_VIDEO, data["content"], "yanlijie", filepath, speed=3, bgm=settings.DUB_BGM)
    return filepath
    
        