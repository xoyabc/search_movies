#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Env: python 2.7.6
# Date: 07/11/2019
import requests
import re
import sys
from bs4 import BeautifulSoup
'''
推荐影片(标红)：疾速备战
普通影片：巴黎野玫瑰
有多个搜索结果：running
'''

try:
    name = sys.argv[1].decode('utf-8')
    
except Exception as e:
    print (e)

url = "http://so.hao6v.com/e/search/index.php"
title = u'{}'.format(name)
submit = u'搜索'.encode('utf-8')
keyboard_gb = title.encode('gb2312')


# 请求参数
payload = {
    'Submit22': submit,
    'keyboard': keyboard_gb,
    'show': 'title,smalltext',
    ' tbname': 'Article',
    'tempid': 1
    }


# 定义 header
headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'cache-control': "no-cache",
    'connection': "keep-alive",
    'content-length': "71",
    'content-type': "application/x-www-form-urlencoded",
    'cookie': "bdshare_firstime=1573047558604; ecmslastsearchtime=1573047798",
    'dnt': "1",
    'host': "so.hao6v.com",
    'origin': "http://so.hao6v.com",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    }

def search_6vdy():
    response = requests.request("POST", url, data=payload, headers=headers)
    html = response.text
    # get title and corresponding link
    soup = BeautifulSoup(html.encode('utf-8'), "html.parser",from_encoding='gb2312')  
    all_result = soup.find_all('span', attrs={"class": "blue14"})
    top_5_result = all_result[0:5]
    print ("Search result link: {}\nStatus code: {}") .format(response.url, response.status_code)
    for item in top_5_result:
        link =  item.a['href']
        title = item.a.text.encode('utf-8')
        real_link = 'http://so.hao6v.com' + link
        print "名称：{} 链接：{}" .format(title, real_link)
    
    '''
    # Method 2, get title and link
    #patten1 = re.compile(r'<span class="blue14"><a href=(.*?) target=_blank>.*?(<font color=\'.*?\'>)?(.*?)(</font>)?</a></span></font></td>', re.S)
    patten1 = re.compile(r'<span class="blue14"><a href=(.*?) target=_blank>([<>/ a-z\'=0-9A-Z#]*)?(.*?)<?[<>/a-z]*?</a></span></font></td>', re.S)
    
    for i in re.findall(patten1, str(html.encode('utf-8')))[0:5]:
        link = i[0]
        title = i[2]
        real_link = 'http://so.hao6v.com' + link
        print "名称：{} 链接：{}" .format(title, real_link)
    '''
    

if __name__ == '__main__':
    search_6vdy()
