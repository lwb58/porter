import os
import datetime
from intl import api
from movpy.api import dub
from porter import intl_data, settings
from toolpy.wrapper import ConsoleScripts

@ConsoleScripts
def fetch_today_news(limit=None):
    '''获取今日经济类新闻'''
    date = str(datetime.datetime.now().date())

    old_days = []
    for _date in intl_data["today_news"]:
        if _date != date:
            old_days.append(_date)
    
    for _date in old_days:
        intl_data["today_news"].pop(_date)

    news = api.fetch_jingji_news(date, limit=limit)
    for i in news:
        print(i["title"])
        if i["url"] not in intl_data["today_news"][date]["jingji"]:
            intl_data["today_news"][date]["jingji"][i["url"]] = i
    print(len(news))


@ConsoleScripts
def gen_news_video():
    '''生成新闻视频'''
    date = str(datetime.datetime.now().date())
    for _, data in intl_data["today_news"][date]["jingji"].items():
        if not data.get("completed"):
            filepath = os.path.join(settings.UPLOAD_PATH, data["title"] + ".mp4")
            content = f'''
            大家好，我是小芳。
            {data["content"]}
            以上就是视频的全部内容。您有什么看法欢迎留言告诉我。
            '''
            dub(settings.DUB_VIDEO, content, "yanlijie",
                filepath, speed=3, bgm=settings.DUB_BGM)
            data["completed"] = True
            return filepath
