
python /root/porter/porter/set_cookies.py

cd /root/movpy
python setup.py install

cd /root/fuck_bilibili
python setup.py install

cd /root/fuck_sina
python setup.py install

cd /root/porter
python setup.py install

cd /root/static
download_sina_dance_videos
gen_dance_video
upload_dance_video_to_bilibili