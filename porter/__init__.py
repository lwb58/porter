
from toolpy.jsonfile import JsonFile
from porter import settings

__all__ = ["jsondata", "bilibili_data", "sina_data", "intl_data"]


jsondata = JsonFile(settings.DATA_PATH).data

bilibili_data = jsondata["bilibili"]
sina_data = jsondata["sina"]
intl_data = jsondata["intl"]