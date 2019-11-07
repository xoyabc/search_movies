#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import sys
import re
from bs4 import BeautifulSoup

try:
    name = sys.argv[1].decode('utf-8')
    
except Exception as e:
    print (e)

url = "http://ys.louxiaohui.com/index.php"
base_url = "https://ys.louxiaohui.com"
title = u'{}'.format(name)
keyboard = title.encode('utf-8')

# 请求参数
querystring = {"m":"vod-search"}

# 请求数据
#payload = "wd=%E7%96%BE%E9%80%9F%E5%A4%87%E6%88%98"
payload = "wd={}".format(keyboard)


# 定义 header
headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'cache-control': "no-cache",
    'connection': "keep-alive",
    'content-length': "57",
    'content-type': "application/x-www-form-urlencoded",
    'dnt': "1",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    }


# 搜索函数
def search_maccms():
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    html = response.text
    soup = BeautifulSoup(html.encode('utf-8'), "html.parser")
    all_result = soup.select('div[class="channel b"] > ul > li')[0:2]
    
    if len(all_result) > 0:
        for i in all_result:
            link = i.select('div[class="l"] > h2 > a')[0]['href'].strip()
            real_link = base_url + link
            name = i.select('div[class="l"] > h2 > a')[0].text.encode('utf-8').strip()
            anchor = i.select('div[class="l"]')[0].find("span", text=re.compile("年份：".decode("utf-8")))
            year = anchor.next_element.next_element.strip()
            print ("{} {} {}".format(name, year, real_link))
    else:
        print ("未找到相关影片，请更换关键词")


if __name__ == '__main__':
    search_maccms()
