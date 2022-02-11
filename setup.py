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
        #  "toolpy": [
        #     'template/*/*',
        # ],
    },
    description='开发工具包的模板',
    author='Tu Weifeng',
    author_email='907391489@qq.com',
    url='https://github.com/tuweifeng',
    platforms="any",
    license='MIT',
    entry_points = {
        'console_scripts': [
            'download_sina_dance_videos = porter.main:download_sina_dance_videos',
            'gen_dance_video = porter.main:gen_dance_video',
            'upload_dance_video_to_bilibili = porter.main:upload_dance_video_to_bilibili',
        ]
    },
    install_requires=[
        # 'PyMySQL<=0.9.3,>=0.9',
        # 'aiomysql==0.0.21'
    ],
    python_requires='',
)
