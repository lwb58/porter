import os

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

DOWNLOAD_PATH = "./download"
UPLOAD_PATH = "/tmp/porter/upload"

if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)


DUB_VIDEO = os.path.join(STATIC_DIR, "media/dub.mp4")
DUB_BGM = os.path.join(STATIC_DIR, "media/dub.mp3")

SUBMIT_BILIBILI_COUNT_KEY = "SUBMIT_BILIBILI_COUNT_KEY"
