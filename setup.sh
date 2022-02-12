
python /root/porter/porter/set_cookies.py

cd /root/movpy
python setup.py install > /dev/null

cd /root/fuck_bilibili
python setup.py install > /dev/null

cd /root/fuck_sina
python setup.py install > /dev/null

cd /root/porter
python setup.py install > /dev/null

cd /root/static
python -u /root/porter/porter/main.py