import os
import sys
import hashlib

from prettytable import PrettyTable as pt

import web
import info

def search(url, keyword, page, pagesize):
    url[1] = keyword
    url[3] = page
    url[5] = pagesize
    url_str = "".join(url)
    result = web.get(url_str)
    result = result["data"]
    if result:
        if type(result) == dict:
            os.system("clear")
            return result
        else:
            print("返回类型错误", type(result))
            sys.exit(1)
    else:
        sys.exit(1)

def searchUI(result):
    song_list = result["info"]
    length = len(song_list)
    table_data = []
    for item in range(length):
        line_data = []
        line_data.append(item)
        line_data.append(song_list[item]["songname"])
        line_data.append(song_list[item]["singername"])
        line_data.append(song_list[item]["album_name"])
        line_data.append(song_list[item]["hash"])
        table_data.append(line_data)
    table = pt()
    table.field_names = ["序号", "歌名", "歌手", "专辑名", "hash"]
    for item in table_data:
        table.add_row(item)
    for field in table.field_names:
        table.align[field] = "c"
    print(table)
    user_choice = input("序号：")
    try:
        user_choice = int(user_choice)
    except ValueError:
        print("请输入序号")
        sys.exit(1)
    if not 0 <= user_choice < length:
        print("请输入有效的序号")
        sys.exit(1)
    return song_list[user_choice]["hash"]

def getInfo(url, song_hash):
    url[1] = song_hash
    url_str = "".join(url)
    result = web.get(url_str)
    if result:
        if type(result) == dict:
            os.system("clear")
            return result
        elif result == "需要付费":
            print("需要付费，无法下载")
            sys.exit(1)
        else:
            print("返回类型错误", type(result), result)
            sys.exit(1)
    else:
        print("返回值为<False>，请提交bug")
        sys.exit(1)

def get_dld_url(url, hash, md5):
    url[1] = hash
    url[3] = md5
    url_str = "".join(url)
    result = web.get(url_str)
    if result:
        if type(result) == dict:
            return result["url"], f"{result['fileName']}.{result['extName']}"
        else:
            print("返回类型错误", type(result))
            sys.exit(1)
    else:
        sys.exit(1)

def md5(string):
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))  # 转为字节并计算
    return md5.hexdigest()  # 返回十六进制字符串

if __name__ == "__main__":
    search_url = ["http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword=", "{关键字}", "&page=", "{页数}", "&pagesize=", "{单页数量}"]
    # 使用result = "".join(search_url)转换成字符串，下同
    info_url = ["http://m.kugou.com/app/i/getSongInfo.php?hash=", "{hash}", "&cmd=playInfo"]
    download_url = ["http://trackercdn.kugou.com/i/?cmd=4&hash=", "{hash}", "&key=", "{MD5({hash}kgcloud)}", "&pid=1&forceDown=0&vip=1"]
    
    print(f"""
{"="*30}
|    KugouMusicDownloader    |
{"="*30}

""")
    page = "1"
    keyword = input("请输入关键字：")
    if not keyword:
        print("请输入关键字")
        sys.exit(1)
    pagesize = input("搜索数量:")
    if not pagesize:
        print("请输入数量")
        sys.exit(1)
    try:
        int(pagesize)
    except ValueError:
        print("请输入数字")
        sys.exit(1)
    
    # 搜索
    search_result = search(search_url, keyword, page, pagesize)
    song_hash = searchUI(search_result)
    # 选择
    song_info = getInfo(info_url, song_hash)
    download_hash = info.main(song_info)
    if not download_hash:
        print("暂无该音质")
        sys.exit(1)
    # 下载
    download_md5 = md5(f"{download_hash}kgcloud")
    dld_url, file_full_name = get_dld_url(download_url, download_hash, download_md5)
    web.download(dld_url, file_full_name)
