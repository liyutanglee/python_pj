#基于python 3.7.0[每日信息推送]

from __future__ import unicode_literals
import time
import platform

from wxpy import *
import requests

import urllib.request
import json

# 获取每日英语励志精句
def get_english_inspirational_aphorism():
    en_r = requests.get("http://open.iciba.com/dsapi/")
    en_note = en_r.json()['note']
    en_content = en_r.json()['content']
    return en_note,en_content

# 获取当前天气信息
def get_current_weather():
    # 天气接口
    we_url = "http://t.weather.sojson.com/api/weather/city/101281106"
    we_content = urllib.request.urlopen(we_url).read()
    we_all_data = json.loads(we_content)

    city_info = we_all_data['cityInfo']
    # 城市信息
    we_city = city_info['city']

    data = we_all_data['data']
    # 当前温度
    we_wendu = data['wendu']
    # 湿度
    we_shidu = data['shidu']
    # 空气质量
    we_quality = data['quality']
    # 感冒指数
    we_ganmao = data['ganmao']

    # 预报信息
    forecast_info = data['forecast']
    today_info = forecast_info[0]
    # 最高气温
    we_high = today_info['high']
    # 最低气温
    we_low = today_info['low']
    # 礼拜
    we_week = today_info['week']
    # 风向
    we_fx = today_info['fx']
    # 风力
    we_fl = today_info['fl']
    # 天气类型
    we_type = today_info['type']
    # 提醒
    we_notice = today_info['notice']

    return ("🗓 -"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n      -{0}\n🏙 -{1}\n🔖 -{2},实时温度:{3}℃\n🌡 -{4}~{5}\n🈯 -空气质量:{6},湿度:{7}\n🎏 -{8},风力{9}\n✔ -{10}.{11}"\
            .format(we_week, we_city, we_type, we_wendu, we_low, we_high, we_quality, we_shidu, we_fx, we_fl, we_ganmao, we_notice))

def get_tencent_new():
    te_url = "https://api.shenjian.io/?appid=86822dc929f8b8d2e7b79a6c69296fa6"
    te_content = urllib.request.urlopen(te_url).read()
    te_all_data = json.loads(te_content)

    outstr = "📋"+time.strftime("%Y-%m-%d", time.localtime())+"午间新闻\n"
    for user in te_all_data['data']:
        outstr = outstr + "💢 - " + user['title'] + "\n链接:" + user['url'] + "\n"

    return outstr

# 发送消息给指定微信
def send_message(your_message):
    try:
        # 对方的微信名称
        send_wx = bot.friends().search(needtosend_wechat_name)[0]
        # 发送消息给对方
        send_wx.send(your_message)
    except:
        # 你的微信名称
        send_wx = bot.friends().search(my_wechat_name)[0]
        # 提示
        send_wx.send(u"信息推送出问题了，赶紧去看看咋回事")



# 在规定时间内进行推送操作
def start_push():

    # 标志位，防止同一时间内重复发送消息
    f_english_inspirational_aphorism = False
    f_current_weather730 = False
    f_current_weather1200 = False
    f_tencent_new = False

    # 待发送的内容，先置为空
    message = ""

    # 死循环
    while(True):
        # 提示
        print("监听中，时间:%s"% time.ctime())

        # 获取时间，只获取时和分，对应的位置为倒数第13位到倒数第8位
        now_time = time.ctime()[-13:-8]

        if (now_time == say_english_inspirational_aphorism):
            if(f_english_inspirational_aphorism == False):
                note, content = get_english_inspirational_aphorism()
                message = "📝 每日英语励志精句\n原文: " + content + "\n\n翻译: " + note
                send_message(message)
                f_english_inspirational_aphorism = True
                f_current_weather730 = False
                f_current_weather1200 = False
                f_tencent_new = False
                print("推送每日英语励志精句:%s" % time.ctime())

        elif (now_time == say_current_weather730):
            if (f_current_weather730 == False):
                message = get_current_weather()
                send_message(message)
                f_english_inspirational_aphorism = False
                f_current_weather730 = True
                f_current_weather1200 = False
                f_tencent_new = False
                print("推送7:30天气信息:%s" % time.ctime())

        elif (now_time == say_current_weather1200):
            if (f_current_weather1200 == False):
                message = get_current_weather()
                send_message(message)
                f_english_inspirational_aphorism = False
                f_current_weather730 = False
                f_current_weather1200 = True
                f_tencent_new = False
                print("推送12:00天气信息:%s" % time.ctime())

        elif (now_time == say_tencent_new):
            if (f_tencent_new == False):
                message = get_tencent_new()
                send_message(message)
                f_english_inspirational_aphorism = False
                f_current_weather730 = False
                f_current_weather1200 = False
                f_tencent_new = True
                print("推送午间新闻信息:%s" % time.ctime())

        # 延时10秒
        time.sleep(10)



if __name__ == "__main__":

    # 启动微信机器人，自动根据操作系统执行不同的指令
    # windows系统或macOS Sierra系统使用bot = Bot()
    # linux系统或macOS Terminal系统使用bot = Bot(console_qr=2)
    print(platform.system());
    if('Windows' in platform.system()):
        # Windows
        bot = Bot()
    elif('Darwin' in platform.system()):
        # MacOSX
        bot = Bot()
    elif('Linux' in platform.system()):
        # Linux
        bot = Bot(console_qr=2,cache_path=True)
    else:
        # 自行确定
        print("无法识别你的操作系统类型，请自己设置")

    # 设置你的微信名称和对方的微信名称，记住，不是微信ID也不是微信备注
    # 你的微信名称，记住，不是微信ID也不是微信备注
    my_wechat_name = u'棠哥仔🍥'
    # 需要发送的微信名称，记住，不是微信ID也不是微信备注
    needtosend_wechat_name = u'棠哥仔🍥'

    # 设置各种信息推送时间
    say_english_inspirational_aphorism = "07:40"
    say_current_weather730 = "07:30"
    say_current_weather1200 = "12:00"
    say_tencent_new = "12:15"


    # 开始信息推送
    start_push()


