#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import sys
import re
import json
from bs4 import BeautifulSoup

'''
1，多页：教父
2，一页: 某种女人
'''

#try:
#    name = sys.argv[1].decode('utf-8')
#    
#except Exception as e:
#    print (e)

url = "http://ys.louxiaohui.com/index.php"
base_url = "http://ys.louxiaohui.com"

# 请求参数
querystring = {"m":"vod-search"}


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


# 生成短链
def gen_short_url(long_url):
    url = 'http://tools.aeink.com/tools/dwz/urldwz.php'
    payload = { 'api': 'urlcn', 'longurl': long_url}
    try:
        resp = requests.get(url, params=payload)
        json_data = json.loads(resp.text)
        short_link = json_data['ae_url']
        return short_link
    except Exception as e:
        short_link = None
    

def get_movie_info(all_result, movie_year):
    for i in all_result:
        link = i.select('div[class="l"] > h2 > a')[0]['href'].encode('utf-8').strip()
        real_link = base_url + link
        tiny_link = gen_short_url(real_link)
        name = i.select('div[class="l"] > h2 > a')[0].text.encode('utf-8').strip()
        year_anchor = i.select('div[class="l"]')[0].find("span", text=re.compile("年份：".decode("utf-8")))
        year = year_anchor.next_element.next_element.encode('utf-8').strip()
        #if name == keyword and int(movie_year) == int(year):
        #if name == keyword:
        if not movie_year:
            if name == keyword:
                print ("{} {} {}".format(name, real_link, tiny_link))
        else:
            if name == keyword and int(movie_year) == int(year):
                print ("{} {} {} {}".format(name, year, real_link, tiny_link))


# 搜索函数
def search_maccms(name, year = None):
    print name,year
    global keyword
    title = u'{}'.format(name.decode('utf-8'))
    #keyword = quote(title.encode('utf-8'))
    keyword = name.decode('utf-8').encode('utf-8')
    # 请求数据
    #payload = "wd=%E7%96%BE%E9%80%9F%E5%A4%87%E6%88%98"
    payload = "wd={}".format(keyword)
    print payload, querystring
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    html = response.text
    soup = BeautifulSoup(html.encode('utf-8'), "html.parser")
    all_result = soup.select('div[class="channel b"] > ul > li')[0:10]
    
    if len(all_result) > 0:
        get_movie_info(all_result, year)
    elif len(all_result) == 0:
        print ("未找到相关影片，请更换关键词")
    # 翻页
    if len(all_result) == 10:
        NEXT_PAGE = True
        try:
            next_page_link = soup.find("a", class_="pagelink_a", text=re.compile("下一页".decode("utf-8")))['href']
            real_next_page_link = base_url + next_page_link
        except Exception as e:
            NEXT_PAGE = False
        while NEXT_PAGE:
            resp = requests.get(real_next_page_link)
            print real_next_page_link
            print (resp)
            html = resp.text
            soup = BeautifulSoup(html.encode('utf-8'), "html.parser")
            all_result = soup.select('div[class="channel b"] > ul > li')[0:10] 
            get_movie_info(all_result, year)
            try:
                next_page_link = soup.find("a", class_="pagelink_a", text=re.compile("下一页".decode("utf-8")))['href']
                real_next_page_link = base_url + next_page_link
            except Exception as e:
                NEXT_PAGE = False


def search_by_movie_name():
    with open('movie.name', 'rU') as f:
        for line in f:
            name = line.split()[0].strip()
            print name
            search_maccms(name)


if __name__ == '__main__':
    search_by_movie_name()
