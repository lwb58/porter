# -*- coding:utf-8 -*-
from porter import sina, intl, bilibili, bilibili_redis, settings



def main():
    count = bilibili_redis.get(settings.SUBMIT_BILIBILI_COUNT_KEY) or 0

    if int(count) % 3 == 0:
        bilibili_cookie = bilibili.get_cookies()
        intl.fetch_today_news()
        video = intl.gen_news_video()
        if video:
            bilibili.submit_video(bilibili_cookie, video, "热点", "社会,国际,打卡挑战,必剪创作")

    else:
        bilibili_cookie = bilibili.get_cookies()
        sina.download_videos("舞蹈", 5)
        video = sina.merge_videos("舞蹈", 2)
        bilibili.submit_video(bilibili_cookie, video, "舞蹈", "舞蹈,打卡挑战,必剪创作")



if __name__ == "__main__":
    main()
