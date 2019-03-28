import os
import re
import json
import time
import requests
from fake_useragent import UserAgent

ua = UserAgent()


def get_song(song_name):
    search_url = "https://songsearch.kugou.com/song_search_v2?callback=jQuery112405132987859127838_1550204317910&page" \
                 "=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_fil" \
                 "ter=0&_=1550204317912&keyword={}".format(song_name)
    headers = {
        "UserAgent": ua.random
    }
    res = requests.get(search_url, headers=headers)
    start = re.search("jQuery\d+_\d+\(?", res.text)
    js = json.loads(res.text.strip().lstrip(start.group()).rstrip(")"))  # 注意：末尾有一个换行需要去掉
    song_list = js['data']['lists']

    songcount=10 if len(song_list)>10 else len(song_list)
    for i in range(songcount):
        print(str(i + 1) + ">>>" + str(song_list[i]['FileName']).replace('<em>', '').replace('</em>', ''))

    num = int(input("\n请输入您想要下载的歌曲序号（0:退出下载重新搜索）："))

    if num==0:
        return
    print("请稍等，下载歌曲中...")
    time.sleep(1)

    file_hash = song_list[num-1]['FileHash']
    songname=str(song_list[num-1]['FileName']).replace('<em>', '').replace('</em>', '').replace(' ', '')
    hash_url = "http://www.kugou.com/yy/index.php?r=play/getdata&hash={}".format(file_hash)
    hash_res = requests.get(hash_url,headers=headers)
    hash_js = hash_res.json()  # json格式
    play_url = hash_js['data']['play_url']

    # 下载歌曲
    try:
        if not os.path.exists('kgmusic'):
            os.mkdir("kgmusic")
        with open("kgmusic/" + songname + ".mp3", "wb")as fp:
            fp.write(requests.get(play_url).content)
        print("歌曲已下载完成！")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    while 1==1:
        get_song(input("请输入您想要搜索的歌曲名称："))
