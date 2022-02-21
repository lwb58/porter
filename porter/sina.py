import os
from movpy.editor import VideoFileClip
from movpy.editor import concate_clips
from sina import api
from sina.base.data import SINA_CHANNEL_CID_MAP
from porter import sina_redis, settings, bilibili_redis
from toolpy.wrapper import ConsoleScripts


@ConsoleScripts
def download_videos(channel, limit=5):
    '''下载新浪视频
    @param: channel
        综艺 美食 游戏 评测 音乐 影视 旅游 娱乐 体育 人文艺术 时尚美妆 动漫 知识 VLOG 搞笑幽默 舞蹈 纪录片
    @param: limit
        限制下载数量
    '''
    assert channel in SINA_CHANNEL_CID_MAP.keys()
    sina_cookies = sina_redis.hget("cookies", "guest")
    videos = api.fetch_channel_videos_playinfo(sina_cookies, channel, limit)
    for video in videos:
        author = video["playinfo"]["author"]
        url = video["playinfo"]["url"]
        title = video["title"]
        author_dir = os.path.join(settings.DOWNLOAD_PATH, author)
        filepath = os.path.join(author_dir, title + ".mp4")

        if not os.path.exists(author_dir):
            os.makedirs(author_dir)

        if not sina_redis.sismember(channel, filepath):
            api.download(sina_cookies, url, filepath)
            sina_redis.zadd(channel, {filepath: 0})


@ConsoleScripts
def merge_videos(channel, limit=2):
    '''拼接新浪视频
    @param: channel
        综艺 美食 游戏 评测 音乐 影视 旅游 娱乐 体育 人文艺术 时尚美妆 动漫 知识 VLOG 搞笑幽默 舞蹈 纪录片
    @param: limit
        限制素材数量
    '''
    assert channel in SINA_CHANNEL_CID_MAP.keys()
    files = sina_redis.zrangebyscore(channel, min=0, max=0, start=0, num=limit)
    assert len(files) == limit
    clips = []

    for file in files:
        print(file)
        sina_redis.zincrby(channel, 1, file)
        clips.append(VideoFileClip(file).audio_fadeout(3))
        os.remove(file)

    bilibili_redis.incr(settings.SUBMIT_BILIBILI_COUNT_KEY, 1)
    count = bilibili_redis.get(settings.SUBMIT_BILIBILI_COUNT_KEY)
    title = f"{os.path.basename(files[0])[:-4]} 第 {int(count) % 1000} 弹"
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


@ConsoleScripts
def get_cookies(key=None):
    '''获取新浪cookie'''
    if key:
        return sina_redis.hget("cookies", key)
    count = bilibili_redis.get(settings.SUBMIT_BILIBILI_COUNT_KEY) or 0
    cookies = sina_redis.hvals("cookies")
    return cookies[int(count) % len(cookies)]


@ConsoleScripts
def set_cookies(key, value):
    '''设置新浪cookie'''
    sina_redis.hset("cookies", key, value)


def main():
    sina_cookies = "SUB=_2AkMWMfo4f8NxqwJRmf0UzGrrb4p3zA7EieKgbQvjJRMxHRl-yT8XqhIitRB6PbHU1x4DelF5m1mgbuUpktR7RBSuBv_i; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhXNkBi.GrGZqSDfvfGD-R3; SINAGLOBAL=8855199877506.115.1634563345055; UOR=,,www.baidu.com; TC-V-WEIBO-G0=b09171a17b2b5a470c42e2f713edace0; _s_tentry=-; Apache=6022133131911.547.1644373611163; ULV=1644373611339:3:1:1:6022133131911.547.1644373611163:1637221914122; XSRF-TOKEN=lpyJU92E7hRY7_BCZKzAAXKb; WBPSESS=CcKh_7VyRZckvS8BGV3cs_dlhmyt0A7SS4WiKq5UIOn9MAuMc9xAW7Qc8N2P6n_TIslU4Iqtyu32rFskxZ1kWsB9fGXPRXZNZioUtrV40L2hE4XhIlIuEdujfKZ-Ysll87QVR66OYWnkv-25CNphaXEpsecDPNXfguuQzwEQAto="
    set_cookies("guest", sina_cookies)


if __name__ == "__main__":
    main()
