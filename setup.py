import os
from setuptools import setup, find_packages

package_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
#  打包
setup(
    name=package_name,
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data = {
         "porter": [
            'static/media/*',
        ],
    },
    description='视频制作、搬运',
    author='Tu Weifeng',
    author_email='907391489@qq.com',
    url='https://github.com/tuweifeng',
    platforms="any",
    license='MIT',
    entry_points = {
        'console_scripts': [
            # intl
            'porter_intl_fetch_today_news  =   porter.intl:fetch_today_news.shell',
            'porter_intl_gen_news_video    =   porter.intl:gen_news_video.shell',
            # sina
            'porter_sina_download_videos   =   porter.sina:download_videos.shell',
            'porter_sina_merge_videos      =   porter.sina:merge_videos.shell',
            'porter_sina_get_cookies       =   porter.sina:get_cookies.shell',
            'porter_sina_set_cookies       =   porter.sina:set_cookies.shell',
            # bilibili
            'porter_bilibili_get_cookies   =   porter.bilibili:get_cookies.shell',
            'porter_bilibili_set_cookies   =   porter.bilibili:set_cookies.shell',
            # task
            'porter_task_1                 =   porter.main:task_1',
            'porter_task_2                 =   porter.main:task_2',
        ]
    },
    install_requires=[
        'redis>=4.1.3'
    ],
    python_requires='>=3.5',
)
