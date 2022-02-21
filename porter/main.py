# -*- coding:utf-8 -*-
from porter import task_sina, task_intl, task_bilibili


def task_1():
    bilibili_cookie = task_bilibili.get_cookies()
    task_sina.download_videos("舞蹈", 5)
    video = task_sina.merge_videos("舞蹈", 2)
    task_bilibili.submit_video(bilibili_cookie, video, "舞蹈", "舞蹈,打卡挑战,必剪创作")


def task_2():
    bilibili_cookie = task_bilibili.get_cookies()
    task_intl.fetch_today_news()
    video = task_intl.gen_news_video()
    task_bilibili.submit_video(bilibili_cookie, video, "热点", "社会,国际,打卡挑战,必剪创作")


def main():
    count = task_bilibili.get_submit_count()
    if count % 3 == 0:
        task_2()
    else:
        task_1()


if __name__ == "__main__":
    main()
