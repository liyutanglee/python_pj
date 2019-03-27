#基于python 3.7.0[根据网易云歌单下载音乐]

import os
import requests
import re
import execjs
import json
from lxml import etree

class Down(object):
    def __init__(self):
        pass
    
    # 计算 ids 的加密后的值（通过引入js文件，计算相应的值）
    def countids(self,ids):
        # 传入的参数，这里指的是获取音乐URL时，需要传入含有该音乐文件ids的字符串。
        ddd = '{"ids":"['+ids+']","level":"standard","encodeType":"aac","csrf_token":""}'
        # 导入js文件
        f=open('countdis.js','r',encoding='utf-8')
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        ctx = execjs.compile(htmlstr)
        f.close()
        # 运行js的 d 函数，并传入参数 ddd，也就是刚才定义的完整字符串，并返回。
        return ctx.call('d', ddd)

    # 获取到该音乐的真实 url 地址
    def geturl(self):
        url = 'https://music.163.com/#/playlist?id=2586250195'
        url = url.replace('/#', '').replace('https', 'http')  # 对字符串进行去空格和转协议处理

        # 请求头
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36','Referer': 'https://music.163.com/','Host': 'music.163.com'}
        # 请求页面的源码
        res = requests.get(url=url, headers=headers).text

        tree = etree.HTML(res)
        # 音乐列表
        song_list = tree.xpath('//ul[@class="f-hide"]/li/a')
        # 歌单页面
        song_list_name_tree = tree.xpath('//h2[contains(@class,"f-ff2")]/text()')
        song_list_name = str(song_list_name_tree[0]) if song_list_name_tree else None

        # 设置音乐下载的文件夹为歌单名
        folder = './' + song_list_name

        if not os.path.exists(folder):
            os.mkdir(folder)

        for i, s in enumerate(song_list):
            try:
                href = str(s.xpath('./@href')[0])
                song_id = href.split('=')[-1]

                # 获取歌曲的歌手
                # ==============================================
                detailurl = 'https://music.163.com/#/song?id='+song_id
                detailurl = detailurl.replace('/#', '').replace('https', 'http')
                detailheaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36','Referer': 'https://music.163.com/', 'Host': 'music.163.com'}
                detailres = requests.get(url=detailurl, headers=detailheaders).text
                detailtree = etree.HTML(detailres)
                singers = detailtree.xpath('//p[@class="des s-fc4"][1]/span/a/text()')
                singersstr = ''
                for x in singers:
                    singersstr = singersstr + "," + x
                #==============================================

                title = str(s.xpath('./text()')[0])  # 音乐的名字
                title = title.replace('/', '-')
                title = title.replace(':', '：')
                title = title.replace('"', '\'')
                title = title + " - " + singersstr[1:]
                filepath = folder + '/' + title

                # 返回的是含有params 和 encSecKey两个加密文的，所以通过列表获取到相应的值。
                stra = self.countids(song_id)
                encSecKey = stra[0]
                params = stra[1]
                _headers = {'Referer': 'https://music.163.com/','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
                _data = {'encSecKey': encSecKey, 'params': params}
                # 把获取到的两个参数值，提交到服务器，获得 URL 地址。
                urltext = requests.post('https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=',headers=_headers, data=_data).text
                _json = json.loads(urltext)
                url = _json['data'][0]['url']
                # 获得URL后，直接使用get下载音乐文件到本地。
                data = requests.get(url, _headers, stream=True)

                with open(filepath + '.mp3', 'wb') as f:
                    for j in data.iter_content(chunk_size=512):
                        f.write(j)
                    print(title+'.mp3 写出完毕!')
            except Exception:
                print(title+"-下载错误！")
            continue


# 运行
if __name__=='__main__':
    bb=Down()
    bb.geturl()
