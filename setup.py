import os
from setuptools import setup, find_packages

package_name = os.path.basename(os.path.dirname(__file__))
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
        # 'console_scripts': [
        #     'toolpy = toolpy.main:main',
        # ]
    },
    install_requires=[
        # 'PyMySQL<=0.9.3,>=0.9',
        # 'aiomysql==0.0.21'
    ],
    python_requires='',
)
