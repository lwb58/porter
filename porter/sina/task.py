import os
import tempfile
import shutil
import random
from movpy.editor import VideoFileClip
from movpy.editor import concate_clips
from sina import api
from sina.base.data import SINA_CHANNEL_CID_MAP
from porter import redis_client, settings


def download_videos(channel, limit=5):
    '''
    @param: channel
        综艺 美食 游戏 评测 音乐 影视 旅游 娱乐 体育 人文艺术 时尚美妆 动漫 知识 VLOG 搞笑幽默 舞蹈 纪录片
    @param: limit
        限制下载数量
    '''
    assert channel in SINA_CHANNEL_CID_MAP.keys()
    sina_cookies = redis_client.hget("sina_cookies", "guest")
    videos = api.fetch_channel_videos_playinfo(sina_cookies, channel, limit)
    for video in videos:
        author = video["playinfo"]["author"]
        url = video["playinfo"]["url"]
        title = video["title"]
        author_dir = os.path.join(settings.DOWNLOAD_PATH, author)
        filepath = os.path.join(author_dir, title + ".mp4")
        if not os.path.exists(author_dir):
            os.makedirs(author_dir)
        if os.path.exists(filepath):
            continue
        else:
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_filepath = os.path.join(tmpdir, title + ".mp4")
                api.download(sina_cookies, url, tmp_filepath)
                shutil.move(tmp_filepath, author_dir)
                redis_client.zadd(channel, {filepath: 0})



def merge_videos(channel, limit=2):
    '''
    @param: channel
        综艺 美食 游戏 评测 音乐 影视 旅游 娱乐 体育 人文艺术 时尚美妆 动漫 知识 VLOG 搞笑幽默 舞蹈 纪录片
    @param: limit
        限制素材数量
    '''
    assert channel in SINA_CHANNEL_CID_MAP.keys()
    files = redis_client.zrange(channel, 0, 5)
    random.shuffle(files)
    clips = []
    authors = []
    print(files)
    for file in files:
        if os.path.exists(file) and os.path.getsize(file) > 0:
            title = os.path.basename(file)[:-4]
            author = os.path.basename(os.path.dirname(file))
            authors.append(author)
            clips.append(VideoFileClip(file).audio_fadeout(3))
            if len(clips) >= limit:
                break
            redis_client.zincrby(channel, 1, file)
        else:
            redis_client.zrem(channel, file)

    redis_client.incr(settings.SUBMIT_BILIBILI_COUNT_KEY, 1)
    count = redis_client.get(settings.SUBMIT_BILIBILI_COUNT_KEY)
    title = f"{title}  第 {int(count) % 1000} 弹"
    filename = os.path.join(settings.UPLOAD_PATH, f"{title}.mp4")
    concate_clips(*clips).write_videofile(
        filename,
        codec='libx264',
        audio_codec='aac',
        logger=None
        # threads=2
    )
    print("merge_videos successful: ", filename)
    return filename