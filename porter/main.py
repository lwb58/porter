# -*- coding:utf-8 -*-
from porter import task_sina, task_intl, task_bilibili, bilibili_data


def task_1():
    bilibili_cookie = task_bilibili.get_cookies("15280371963")
    task_sina.download_videos("舞蹈", 5)
    video = task_sina.merge_videos("舞蹈", 2)
    task_bilibili.submit_video(bilibili_cookie, video, "舞蹈", "舞蹈,打卡挑战")


def task_2():
    bilibili_cookie = task_bilibili.get_cookies("13123371380")
    task_intl.fetch_today_news()
    video = task_intl.gen_news_video()
    if video:
        task_bilibili.submit_video(bilibili_cookie, video, "热点", "社会,国际,打卡挑战,社会观察局,星海计划,知识分享官")


def main():
    bilibili_data.setdefault("task1_count", 0)
    bilibili_data["task1_count"] += 1
    if bilibili_data["task1_count"] % 3 == 0:
        task_2()
    else:
        task_1()
    print("投稿结束！")
    exit(0)


if __name__ == "__main__":
    main()
