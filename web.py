import os
import requests as r
from urllib.request import urlretrieve

def get(url):
    """
        用于请求json
        传入url
        返回string或bool
    """
    try:
        response = r.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        print("请求出错:", e)
        return False
    data = response.json()
    if data["status"] == 0:
        return data["error"]
    elif data["status"] == 1:
        return data
    else:
        print("状态码错误")
        return False

def _progress_hook(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    print(f"下载进度: {percent}%", end="\r")
def download(url, filename):
    urlretrieve(url, filename, reporthook=_progress_hook)
