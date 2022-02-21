# -*- coding:utf-8 -*-
from porter import sina, intl, bilibili


def task_1():
    bilibili_cookie = bilibili.get_cookies()
    sina.download_videos("舞蹈", 5)
    video = sina.merge_videos("舞蹈", 2)
    bilibili.submit_video(bilibili_cookie, video, "舞蹈", "舞蹈,打卡挑战,必剪创作")


def task_2():
    bilibili_cookie = bilibili.get_cookies()
    intl.fetch_today_news()
    video = intl.gen_news_video()
    bilibili.submit_video(bilibili_cookie, video, "热点", "社会,国际,打卡挑战,必剪创作")


def main():
    count = bilibili.get_submit_count()
    if count % 3 == 0:
        task_2()
    else:
        task_1()


if __name__ == "__main__":
    main()
