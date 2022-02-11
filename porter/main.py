# -*- coding:utf-8 -*-
import os
import random
import redis
from sina import api as sina_api
from bilibili import api as bilibili_api
from movpy.editor import *

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

DANCE_VIDEOS_KEY = "dance_videos"
SUBMIT_BILIBILI_COUNT_KEY = "submit_bilibili_count"
UPLOAD_DANCE_PATH = "upload/dance"
DOWNLOAD_DANCE_PATH = "download/dance"


def submit_video_to_bilibili(cookies, filename, title, tid, tag, desc=""):
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


def download_sina_dance_videos():
    count = 5
    sina_cookies = r.hget("sina_cookies", "guest")
    videos = sina_api.fetch_channel_videos_playinfo(sina_cookies, "舞蹈", count)
    for video in videos:
        author = video["playinfo"]["author"]
        url = video["playinfo"]["url"]
        title = video["title"] 
        author_dir = os.path.join(DOWNLOAD_DANCE_PATH, author)
        filepath = os.path.join(author_dir, title + ".mp4")
        if not os.path.exists(author_dir):
            os.makedirs(author_dir) 
        if os.path.exists(filepath):
            continue
        else:
            sina_api.download(sina_cookies, url, filepath)
            r.zadd(DANCE_VIDEOS_KEY, {filepath: 0})
            

def gen_dance_video():
    files = r.zrange(DANCE_VIDEOS_KEY, 0, 5)
    random.shuffle(files)
    files = files[:3]
    clips = []
    authors = []
    for file in files:
        if os.path.exists(file):
            title = os.path.basename(file)
            author = os.path.basename(os.path.dirname(file))
            authors.append(author)
            clips.append(VideoFileClip(file).audio_fadeout(3))
            r.zincrby(DANCE_VIDEOS_KEY, 1, file)
        else:
            r.zrem(DANCE_VIDEOS_KEY, file)

    r.incr(SUBMIT_BILIBILI_COUNT_KEY, 1)
    count = r.get(SUBMIT_BILIBILI_COUNT_KEY)
    if not os.path.exists(UPLOAD_DANCE_PATH):
        os.makedirs(UPLOAD_DANCE_PATH)
    title = f"{' | '.join(authors) } | 第 {count} 弹"
    filename = os.path.join(UPLOAD_DANCE_PATH, f"{title}.mp4")
    concate_clips(*clips).write_videofile(
        filename,
        codec='libx264',
        audio_codec='aac',
        # logger=None
    )


def upload_dance_video_to_bilibili():
    bilibili_cookies = r.hvals("bilibili_cookies")
    count = r.get(SUBMIT_BILIBILI_COUNT_KEY)
    bilibili_cookies = bilibili_cookies[count % len(bilibili_cookies)]
    filepath = ""
    title = ""
    for file in os.listdir(UPLOAD_DANCE_PATH):
        if os.path.isfile(file) and file.endswith(".mp4"):
            filepath = os.path.join(UPLOAD_DANCE_PATH, file)
            title = file[:-4]
            break
    if filepath:
        try:
            submit_video_to_bilibili(bilibili_cookies, filepath, title, 154, "舞蹈,打卡挑战")
        except Exception as e:
            raise e
        finally:
            os.remove(filepath)



def main():
    pass

if __name__ == "__main__":
    main()