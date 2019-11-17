#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import sys
import re
import json
import random
import time
from urllib import quote
from bs4 import BeautifulSoup
# solve SNIMissingWarning, InsecurePlatformWarning on urllib3 when using < Python 2.7.9
import urllib3
urllib3.disable_warnings()
'''
1，多页：教父
2，一页: 某种女人
'''

file = 'movie.name'
url = "http://ys.louxiaohui.com/index.php"
base_url = "https://ys.louxiaohui.com"

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
    #url = 'http://tools.aeink.com/tools/dwz/urldwz.php'
    #payload = { 'api': 'dwzmn', 'longurl': long_url}
    url = "http://sa.sogou.com/gettiny"
    payload = {'url': long_url}
    try:
        resp = requests.get(url, params=payload)
        #print resp.text
        #json_data = json.loads(resp.text)
        short_link = resp.text.strip()
    except Exception as e:
        short_link = None
    finally:
        return short_link

# 发送get请求
def get_one(request_url):
    # add verify=False to solve 'SSLError(CertificateError'
    resp = requests.get(request_url, verify=False)
    html = resp.text
    soup = BeautifulSoup(html.encode('utf-8'), "html.parser")
    return soup


def get_movie_info(all_result, movie_year):
    for i in all_result:
        link = i.select('div[class="l"] > h2 > a')[0]['href'].encode('utf-8').strip()
        real_link = base_url + link
        tiny_link = gen_short_url(real_link)
        name = i.select('div[class="l"] > h2 > a')[0].text.encode('utf-8').strip()
        year_anchor = i.select('div[class="l"]')[0].find("span", text=re.compile("年份：".decode("utf-8")))
        year = year_anchor.next_element.next_element.encode('utf-8').strip()
        movie_msg = None
        if not movie_year:
            if name == keyword:
                #movie_msg = "{} {} {} {}".format(name, year, real_link, tiny_link)
                movie_msg = "[{}][{}]\n{}".format(name, year, tiny_link)
                return movie_msg
                break
        else:
            if name == keyword and int(movie_year) == int(year):
                #movie_msg = "{} {} {} {}".format(name, year, real_link, tiny_link)
                movie_msg = "[{}][{}]\n{}".format(name, year, tiny_link)
                return movie_msg
                break


# 搜索影片
def search_maccms(name, year = None):
    #print name,year
    global keyword
    global movie_info
    try:
        keyword = name.decode('utf-8').encode('utf-8')
    except:
        keyword = name.encode('utf-8')
    movie_info = None
    # 请求数据
    #payload = "wd=%E7%96%BE%E9%80%9F%E5%A4%87%E6%88%98"
    payload = "wd={}".format(keyword)
    #print payload, querystring
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    html = response.text
    soup = BeautifulSoup(html.encode('utf-8'), "html.parser")
    all_result = soup.select('div[class="channel b"] > ul > li')[0:10]
    if len(all_result) > 0:
        movie_info = get_movie_info(all_result, year)
        #print movie_info
    elif len(all_result) == 0:
        pass
        #print ("未找到相关影片，请更换关键词")
    # 翻页，单独一个 if，避免结果数小于 9 时，执行提取下一页链接的 try 语句
    if len(all_result) >= 9:
        NEXT_PAGE = True
        NEXT_MOVIE = True if not get_movie_info(all_result, year) else False
        #print "NEXT_MOVIE: {}".format(NEXT_MOVIE)
        try:
            next_page_link = soup.find("a", class_="pagelink_a", text=re.compile("下一页".decode("utf-8")))['href']
            real_next_page_link = base_url + next_page_link
        except Exception as e:
            NEXT_PAGE = False
        while NEXT_PAGE and NEXT_MOVIE:
            #print real_next_page_link
            soup = get_one(real_next_page_link)
            all_result = soup.select('div[class="channel b"] > ul > li')[0:10] 
            movie_info = get_movie_info(all_result, year)
            #print movie_info
            NEXT_MOVIE = True if not get_movie_info(all_result, year) else False
            try:
                next_page_link = soup.find("a", class_="pagelink_a", text=re.compile("下一页".decode("utf-8")))['href']
                real_next_page_link = base_url + next_page_link
            except Exception as e:
                NEXT_PAGE = False
    return movie_info


# 豆瓣口碑榜
def get_db_mv_week():
    url = 'https://movie.douban.com/chart'
    soup = get_one(url)
    MESSAGE = """
*** 本周豆瓣口碑榜 start ***
{}*** 本周豆瓣口碑榜 end *** 
"""
    contents = []
    for i in soup.select('#listCont2 > li[class="clearfix"] > div[class="name"]'):
        name = i.a.text.strip()
        link = i.a['href'].strip()
        year_soup = get_one(link)
        # get year
        year = re.sub(r'(\(|\))', '', year_soup.select('span[class="year"]')[0].text)
        # get release date and region
        pattern = re.compile(r'(?P<r_date>.*)\((?P<r_region>.*)\)')
        release_date = r_date = r_region = None
        ab_value = 0
        # 距上映已过/还有多少天，90天内的排除
        ts_now = int(time.time())
        safe_interval = 24*3600*90 
        try:
            for date in year_soup.select('span[property="v:initialReleaseDate"]'):
                r_date = pattern.search(date.text).group('r_date')
                r_region = pattern.search(date.text).group('r_region').encode('utf-8')
                format_time = r_date + ' 00:00:00'
                ts = time.strptime(format_time, "%Y-%m-%d %H:%M:%S")
                ts_r_date = int(time.mktime(ts))
                ab_value = abs(ts_now-ts_r_date)
                if '中国大陆'.decode('utf-8').encode("utf-8") in r_region and ab_value <= safe_interval:
                    release_date = r_date
        except:
            pass
        if not release_date:
            #print i.a['href'],name,year,release_date,r_date,r_region,"已上映" + str(ab_value/86400) + "天"
            #print i.a['href'],name,year
            content = str(search_maccms(name, year)) + "\n" if search_maccms(name, year) else ''
            contents.append(content)
            time.sleep(1 + random.randint(1, 3))
    send_msg = MESSAGE.format("".join(contents))
    print send_msg


def search_by_movie_name():
    MESSAGE = """
*** 新片/经典 start ***
{}*** 新片/经典 end *** 
"""
    contents = []
    with open(file, 'rU') as f:
        for line in f:
            name = line.split()[0].strip()
            content = str(search_maccms(name)) + "\n" if search_maccms(name) else ''
            contents.append(content)
    send_msg = MESSAGE.format("".join(contents))
    print send_msg


if __name__ == '__main__':
    try:
        name = sys.argv[1]
        content = search_maccms(name)
        print content
    except Exception as e:
        get_db_mv_week()
        search_by_movie_name()
