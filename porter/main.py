# -*- coding:utf-8 -*-
import os
import re
from bilibili import api as bilibili_api
from bilibili.base.data import TAG_MAP
from porter.sina import task as sina_task
from porter.intl import task as intl_task
from porter import redis_client, settings


def submit_video_to_bilibili(cookies, filename, channel, tag="", desc=""):
    # b站视频标题只允许由中文、英文、数字、日文等可见字符组成
    # 中文       \u4e00-\u9fa5
    # 日文 平假名 \u3040-\u309f
    # 日文 片假名 \u30a0-\u30ff
    # 韩文       \uac00-\ud7ff
    # 非字母数字  \W
    # 字母数字    a-zA-Z0-9 
    assert channel in TAG_MAP.keys()
    tid = TAG_MAP[channel]["tid"]
    tag = tag or TAG_MAP[channel]["tags"]
    title = os.path.basename(filename)[:-4]
    title = "".join(re.findall(r'[\u4e00-\u9fa5 | \u30a0-\u30ff | \u3040-\u309f | a-zA-Z0-9 | \W]+', title))
    info = {
        "copyright": 1,  # 1:有版权  2:无
        "videos": [{
            "filename": filename,
            "title": title,
            "desc": "",
        }],
        "no_reprint": 1,  # 1：不允许转载  0：允许转载
        "interactive": 0,
        "tid": tid,
        "cover": "",  # 由b站返回封面文件名 可以为空，b站会从视频里取一帧作为封面
        "title": title,
        "tag": tag,  # 视频标签
        "desc_format_id": 0,
        "desc": desc,
        "dynamic": "",
        "open_elec": 1,  # 1：开启充电面板 0：不开启
        "subtitle": {
            "open": 0,  # 不开字幕
            "lan": "zh-CN"
        },
        "up_selection_reply": False,
        "up_close_reply": False,
        "up_close_danmu": False,
        "act_reserve_create": 0,
    }
    res = bilibili_api.submit_video(cookies, info)
    print(res)
        


def get_bilibili_cookies(key=None):
    if key:
        return redis_client.hget("bilibili_cookies", key)
    count = redis_client.get(settings.SUBMIT_BILIBILI_COUNT_KEY)
    bilibili_cookies = redis_client.hvals("bilibili_cookies")
    return bilibili_cookies[count % len(bilibili_cookies)]


def main():
    bilibili_cookie = get_bilibili_cookies()

    sina_task.download_videos("舞蹈", 5)
    video = sina_task.merge_videos("舞蹈", 2)
    submit_video_to_bilibili(bilibili_cookie, video, "舞蹈", "舞蹈,打卡挑战,必剪创作")

    intl_task.fetch_today_news()
    video = intl_task.gen_news_video()
    if video:
        submit_video_to_bilibili(bilibili_cookie, video, "热点", "社会,国际,打卡挑战,必剪创作")



if __name__ == "__main__":
    main()
