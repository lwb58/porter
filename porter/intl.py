import os
import json
import datetime
from intl import api
from movpy.api import dub
from porter import intl_redis, settings
from toolpy.wrapper import ConsoleScripts

@ConsoleScripts
def fetch_today_news(limit=None):
    '''获取今日经济类新闻'''
    date = str(datetime.datetime.now().date())
    for i in api.fetch_jingji_news(date, limit=limit):
        if not intl_redis.hexists("jingji_set", i["url"]):
            print(i)
            intl_redis.hset("jingji_set", i["url"], json.dumps(i))
            intl_redis.lpush("jingji_list", i["url"])

@ConsoleScripts
def gen_news_video():
    '''生成新闻视频'''
    url = intl_redis.rpop("jingji_list")
    if url:
        data = intl_redis.hget("jingji_set", url)
        data = json.loads(data)
        filepath = os.path.join(settings.UPLOAD_PATH, data["title"] + ".mp4")
        content = f'''
        大家好，我是小芳。
        {data["content"]}
        以上就是视频的全部内容。您有什么看法欢迎留言告诉我。
        '''
        dub(settings.DUB_VIDEO, content, "yanlijie",
            filepath, speed=3, bgm=settings.DUB_BGM)
        return filepath
