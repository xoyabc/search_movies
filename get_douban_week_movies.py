#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import os
import re
import json
import random
import time
from urllib import quote, quote_plus
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
# solve SNIMissingWarning, InsecurePlatformWarning on urllib3 when using < Python 2.7.9
import urllib3
urllib3.disable_warnings()
# solve UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-4: ordinal not in range(128)
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
'''
1，一页: 某种女人
2，多页：教父
3，无上映日期信息
https://movie.douban.com/subject/4436880/
'''

#url = "http://ys.louxiaohui.com/index.php"
#base_url = "https://ys.louxiaohui.com"
url = "http://vowys.xyz/index.php"
base_url = "https://vowys.xyz"
BASEPATH = os.path.realpath(os.path.dirname(__file__))
douban_weekly_movies = BASEPATH + os.sep + 'douban_weekly_movies.list'
receivers = [
'1031138448@qq.com',
#'842781226@qq.com',
#'3522989840@qq.com',
]

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


douban_headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
     'Accept-Encoding': 'gzip, deflate, sdch',
     'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,en-GB;q=0.2,zh-TW;q=0.2',
     'Connection': 'keep-alive',
     'DNT': '1',
     'HOST': 'movie.douban.com',
     'Cookie': 'iv5LdR0AXBc'
}

tiny_headers = { 'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36" }

# 生成短链
def gen_short_url(long_url):
    #url = "http://sa.sogou.com/gettiny"
    #payload = {'url': long_url}
    long_url = quote_plus(long_url)
    url = "http://tny.im/yourls-api.php"
    payload = {'url': long_url, 'action': 'shorturl', 'format': 'simple'}
    try:
        #resp = requests.get(url, params=payload)
        resp = requests.get(url, params=payload, headers=tiny_headers)
        #print resp.text
        short_link = resp.text.strip()
    except Exception as e:
        short_link = None
    finally:
        return short_link

# 发邮件
def send_mail(receivers, mail_content):
    host_server = 'smtp.yeah.net'
    sender_qq = 'vowys2019@yeah.net'
    pwd = 'vowys2019'
    sender_qq_mail = 'vowys2019@yeah.net'
    #receivers = ['1031138448@qq.com']
    #mail_content = '你好，这是使用 python 发邮件的测试'
    #mail_content = '一周口碑榜'
    mail_title = '一周口碑榜'
    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = Header("也曾鲜衣怒马年少时", 'utf-8') 
    try:
        smtp = SMTP_SSL(host_server)
        smtp.set_debuglevel(1)
        smtp.ehlo(host_server)
        smtp.login(sender_qq, pwd)
        smtp.sendmail(sender_qq_mail, receivers, msg.as_string())
        smtp.quit()
    except Exception as e:
        print('error',e) 


# 发送get请求
def get_one(request_url, headers=None):
    # add verify=False to solve 'SSLError(CertificateError'
    resp = requests.get(request_url, headers=headers, verify=False)
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


def search_from_file(filename, key_word, filed_num):
    with open (filename, 'rU') as f:
        for line in f:
            if key_word == line.strip().split()[filed_num]:
                return True
        return False 


def save_file(filename, content):
    with open (filename, 'a+') as f:
        f.write(content + "\n") 


# 豆瓣口碑榜
def get_db_mv_week():
    cur_date = time.strftime('%Y-%m-%d')
    url = 'https://movie.douban.com/chart'
    soup = get_one(url, headers=douban_headers)
    MESSAGE = """
（链接需要复制到浏览器后打开）
*** 本周豆瓣口碑榜 start ***
{}*** 本周豆瓣口碑榜 end *** 
"""
    contents = []
    for i in soup.select('#listCont2 > li[class="clearfix"] > div[class="name"]'):
        link = i.a['href'].strip()
        # 之前发过的口碑榜影片不再发
        if not search_from_file(douban_weekly_movies, link, 1):
            name = i.a.text.strip()
            year_soup = get_one(link, headers=douban_headers)
            # get year
            year = re.sub(r'(\(|\))', '', year_soup.select('span[class="year"]')[0].text)
            # get release date and region
            pattern = re.compile(r'(?P<r_date>.*)\((?P<r_region>.*)\)')
            release_date = r_date = r_region = None
            ab_value = None
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
            if not ab_value:
                release_info = '无上映信息或尚未上映'
            else:
                release_info = "已上映" + str(ab_value/86400) + "天"
            if not release_date:
                print i.a['href'],name,year,release_date,r_date,r_region,release_info
                print i.a['href'],name,year
                content = str(search_maccms(name, year)) + "\n" if search_maccms(name, year) else ''
                contents.append(content)
                time.sleep(105 + random.randint(1, 5))
            # 查找成功且短链生成后将日期及链接写入到文件
            save_file(douban_weekly_movies, cur_date + ' ' + str(link))
    send_msg = MESSAGE.format("".join(contents))
    # 有新影片时发送邮件
    if len(contents) > 0:
        send_mail(receivers, send_msg)
    print send_msg


if __name__ == '__main__':
    get_db_mv_week()
