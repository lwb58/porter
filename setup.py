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
            'fetch_today_news = porter.intl.task:fetch_today_news',
            'gen_news_video = porter.intl.task:gen_news_video'
        ]
    },
    install_requires=[
        'redis>=4.1.3'
    ],
    python_requires='>=3.5',
)
