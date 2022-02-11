import redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def a():
    bilibili_cookies = "_uuid=F3846222-EDAD-6B5A-7FA8-9FF4F26B16CB51047infoc; buvid3=195A042F-86D0-4FA5-8383-308F1E5C0AED167614infoc; blackside_state=1; rpdid=|(Rlllk)lJ)0J'uYJRJkJJRY; fingerprint_s=da3a2638c24dcca6b74258261428ccd8; LIVE_BUVID=AUTO5716358409259242; PVID=1; fingerprint=79eac04582f75e05c84f486913f2a173; buvid_fp_plain=CA3E8107-D4DD-434A-9C2C-79F6F0B00C5B148804infoc; SESSDATA=50ed2a21%2C1652951349%2C17fad%2Ab1; bili_jct=1f15d82812474b5265bf304ab4692aed; DedeUserID=30784374; DedeUserID__ckMd5=7bdf9ca5dbe22cdd; sid=76zhkfa3; video_page_version=v_old_home; bsource=search_baidu; fingerprint3=13218a4955b4eb32d3fb75d74e13e063; CURRENT_BLACKGAP=1; CURRENT_FNVAL=80; CURRENT_QUALITY=0; innersign=0; i-wanna-go-back=-1; b_ut=5; b_lsid=A6712E62_17ED9125187; buvid_fp=a78d307997c2d2d15b68f6ac90018e18; buvid4=B858F982-52B9-D052-66A0-2B4E55DE503265029-022020819-PFJkqvvsrkqgERnDm+/ksg%3D%3D"
    sina_cookies = "SUB=_2AkMWMfo4f8NxqwJRmf0UzGrrb4p3zA7EieKgbQvjJRMxHRl-yT8XqhIitRB6PbHU1x4DelF5m1mgbuUpktR7RBSuBv_i; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhXNkBi.GrGZqSDfvfGD-R3; SINAGLOBAL=8855199877506.115.1634563345055; UOR=,,www.baidu.com; TC-V-WEIBO-G0=b09171a17b2b5a470c42e2f713edace0; _s_tentry=-; Apache=6022133131911.547.1644373611163; ULV=1644373611339:3:1:1:6022133131911.547.1644373611163:1637221914122; XSRF-TOKEN=lpyJU92E7hRY7_BCZKzAAXKb; WBPSESS=CcKh_7VyRZckvS8BGV3cs_dlhmyt0A7SS4WiKq5UIOn9MAuMc9xAW7Qc8N2P6n_TIslU4Iqtyu32rFskxZ1kWsB9fGXPRXZNZioUtrV40L2hE4XhIlIuEdujfKZ-Ysll87QVR66OYWnkv-25CNphaXEpsecDPNXfguuQzwEQAto="

    r.hset("bilibili_cookies", "13123371380", bilibili_cookies)
    r.hset("sina_cookies", "guest", sina_cookies)

def b():
    cookies = r.hget("sina_cookies", "guests")
    print(cookies)

def c():
    r.zadd("test_zadd", {"twf": 1, "lwf":3, "ttt":2} )

def d():
    r.zincrby("test_zadd", 1, "twf")

def e():
    s = r.zrange("test_zadd", 0, 4, withscores=True)
    print(s)

def f():
    r.zrem("test_zadd", "twf")

# r.set("dance", 1)
# r.incr("dances", 1)
# print(r.get("dances"))

# print(sum([]))
a()