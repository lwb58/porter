
import os
import re
from bilibili import api
from bilibili.base.data import TAG_MAP
from porter import bilibili_redis, settings
from toolpy.wrapper import ConsoleScripts


@ConsoleScripts
def submit_video(cookies, filename, channel, tag="", desc=""):
    '''投稿b站视频
    @param: channel 
        频道
        综艺 美食 游戏 评测 音乐 影视 旅游 娱乐 体育 人文艺术 时尚美妆 动漫 知识 VLOG 搞笑幽默 舞蹈 纪录片
    @param: tag
        标签 egg: 社会,国际,打卡挑战,必剪创作
    @param: desc
        描述
    '''
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
    title = "".join(re.findall(
        r'[\u4e00-\u9fa5 | \u30a0-\u30ff | \u3040-\u309f | a-zA-Z0-9 | \W]+', title))
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
    res = api.submit_video(cookies, info)
    print(res)
    bilibili_redis.incr(settings.SUBMIT_BILIBILI_COUNT_KEY, 1)
    return res


@ConsoleScripts
def get_cookies(key=None):
    '''获取b站cookie'''
    if key:
        return bilibili_redis.hget("cookies", key)
    cookies = bilibili_redis.hvals("cookies")
    count = get_submit_count()
    return cookies[count % len(cookies)]


@ConsoleScripts
def set_cookies(key, value):
    '''设置b站cookie'''
    bilibili_redis.hset("cookies", key, value)


def get_submit_count():
    if not bilibili_redis.get(settings.SUBMIT_BILIBILI_COUNT_KEY):
        bilibili_redis.incr(settings.SUBMIT_BILIBILI_COUNT_KEY, 1)
    return int(bilibili_redis.get(settings.SUBMIT_BILIBILI_COUNT_KEY))


# -*- coding:utf-8 -*-

def main():
    bilibili_cookies_13123371380 = "innersign=0; buvid3=E0EBADF5-3611-3D29-21AC-6C3F4D085F8572855infoc; i-wanna-go-back=-1; b_ut=7; b_lsid=E6310BA21_17EED62AA32; _uuid=1FC1FEB8-7DC5-10DF4-68210-A223DE10DE108C73372infoc; buvid4=1B853BFD-712E-29C7-C15E-D81797377F5174550-022021218-Xp0F8TwTz1KVj+hijssZnQ%3D%3D; fingerprint=a78d307997c2d2d15b68f6ac90018e18; buvid_fp_plain=undefined; SESSDATA=d1c63cc2%2C1660212189%2C35259%2A21; bili_jct=c9ed89cb97091745c5e7f05bf3e52fdf; DedeUserID=30784374; DedeUserID__ckMd5=7bdf9ca5dbe22cdd; sid=c29ugk0v; buvid_fp=a78d307997c2d2d15b68f6ac90018e18"
    bilibili_cookies_15280371963 = "_uuid=F3846222-EDAD-6B5A-7FA8-9FF4F26B16CB51047infoc; buvid3=195A042F-86D0-4FA5-8383-308F1E5C0AED167614infoc; blackside_state=1; rpdid=|(Rlllk)lJ)0J'uYJRJkJJRY; fingerprint_s=da3a2638c24dcca6b74258261428ccd8; LIVE_BUVID=AUTO5716358409259242; PVID=1; video_page_version=v_old_home; bsource=search_baidu; fingerprint3=13218a4955b4eb32d3fb75d74e13e063; CURRENT_FNVAL=80; CURRENT_QUALITY=0; innersign=0; i-wanna-go-back=-1; buvid4=B858F982-52B9-D052-66A0-2B4E55DE503265029-022020819-PFJkqvvsrkqgERnDm+/ksg%3D%3D; CURRENT_BLACKGAP=0; fingerprint=6a47d5395f6b5f4569832fd4306a1258; buvid_fp_plain=undefined; bp_video_offset_1913490337=undefined; b_lsid=41064F6EF_17EED15C83D; SESSDATA=ee202440%2C1660207492%2C1f5b9%2A21; bili_jct=c7b9599a5889230f25ad99156c693856; DedeUserID=1913490337; DedeUserID__ckMd5=47c6454cfc83ffd1; sid=5yqb4znu; b_ut=5; buvid_fp=a78d307997c2d2d15b68f6ac90018e18"

    set_cookies("13123371380", bilibili_cookies_13123371380)
    set_cookies("15280371963", bilibili_cookies_15280371963)


if __name__ == "__main__":
    main()
