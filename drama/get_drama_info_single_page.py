#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re  
import sys  
import urllib  
import requests
import random
import json
import csv
import codecs
from urllib import unquote
from decimal import Decimal
from headers_config import USERAGENT_CONFIG
import time

# logging
import os
import logging
from logging.handlers import TimedRotatingFileHandler

reload(sys)
sys.setdefaultencoding("utf-8")
import urllib3
urllib3.disable_warnings()


BASEPATH = os.path.realpath(os.path.dirname(__file__))
LOGPATH = BASEPATH + os.sep + 'log'
LOGFILE = LOGPATH + os.sep + 'post_data.log'
CSVPATH = BASEPATH + os.sep + 'csv'


# header content
douban_headers = {
     'Host': 'm.dianping.com',
     'Connection': 'keep-alive',
     'Cache-Control': 'max-age=0',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
     'Accept-Encoding': 'gzip, deflate, br',
     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


#show_header = {
#    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
#}


show_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'm.dianping.com',
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
}


show_header_wx = {
        'Host': 'wx.maoyan.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'X-Requested-With': 'wxapp',
        'content-type': 'multipart/form-data',
        'version': 'wallet-v2.14.9',
        'x-wxa-page': 'pages/show/list/index',
        'x-wxa-query': '%7B%22categoryId%22%3A%224%22%7D',
        'x-wxa-referer': 'pages/show/index/index',
        'Referer': 'https://servicewechat.com/wxdbb4c5f1b8ee7da1/902/page-frame.html',
        'Accept-Encoding': 'gzip, deflate, br'
}


add_headers = {
    "content-type": "application/json",
    'authorization': "Bearer 3e64llBnvbd6542gdifkso22vvv_32uy5Mt09h",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.26 Safari/537.36",
    "host": "piao-6gtumoevea8bb36a-1306331692.ap-shanghai.app.tcloudbase.com"
}


# write to csv file
def write_to_csv(filename, head_line, *info_list):
    with open(filename, 'w') as f:
        f.write(codecs.BOM_UTF8)
        writer = csv.writer(f)
        writer.writerow(head_line.split('\t'))
        for row in info_list:
            row_list = row.split('\t')
            writer.writerow(row_list)


def myLog():
    log_fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    formatter = logging.Formatter(log_fmt)
    formatter.datefmt = '%a, %d %b %Y %H:%M:%S'
    # 创建TimedRotatingFileHandler对象
    log_file_handler = TimedRotatingFileHandler(
        filename=LOGFILE, when="midnight", interval=1, backupCount=31)
    log_file_handler.suffix = "%Y-%m-%d.log"
    log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    log_file_handler.setFormatter(formatter)
    log_file_handler.setLevel(logging.DEBUG)

    # 日志标准输出
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log.addHandler(log_file_handler)
    return log


# store the drama info to file
def store_to_file(f,**DICT):
    fd = open(f, 'w')
    try:
        fd.write(json.dumps(DICT))
    except Exception as e:
        err_msg = "Write error,errmsg: {}" .format(e)
        print err_msg
    finally:
        fd.close()


def random_sleep(s, e):
    sleeptime = random.uniform(s, e)
    sleeptime = Decimal(sleeptime).quantize(Decimal('0.00'))
    time.sleep(sleeptime)


# convert date to timestamp
def _to_timestamp(dt):
    timeArray = time.strptime(dt, "%Y.%m.%d")   
    ts = time.mktime(timeArray)
    return ts


# convert timestamp to date
def _to_date(ts):
    timeArray = time.localtime(ts)  
    dt = time.strftime("%Y%m%d", timeArray)
    return dt


def get_start_end_time(t):
    if '-' in t:
        # 2021.7.30 - 2021.8.1
        dt_start = t.split('-')[0].strip()
        dt_end = t.split('-')[1].strip()
    elif '/' in t:
        # 2021.7.16 / 7.17
        pattern = re.compile(r'(?P<year>\d{4})\.(?P<m_start>\d{1,2})\.(?P<d_start>\d{1,2})[^0-9\.]*(?P<m_end>\d{1,2})\.(?P<d_end>\d{1,2})')
        year = pattern.search(t).group('year')
        dt_start = t.split('/')[0].strip()
        dt_end = "{0}.{1}" .format(year, t.split('/')[1].strip())
    elif '周' in t and ':' in t:
        # 2021.8.19 19:30 周四
        dt_start = dt_end = t.split()[0].strip()
    else:
        dt_start = dt_end = 'N/A'
        return dt_start, dt_end, False
    return dt_start, dt_end, True


def get_date_list(s_time, e_time, flag=False):
    l_date = []
    if flag:
        interval_secs = 365*24*60*60
        ts_start = ts_today if (ts_today - _to_timestamp(s_time)) > interval_secs else _to_timestamp(s_time)
        ts_end = _to_timestamp(e_time)
        while ts_start <= ts_end:
            timeArray = time.localtime(ts_start)
            dt_new = time.strftime("%Y年%m月%d日", timeArray)
            l_date.append(dt_new.decode('utf-8'))
            ts_start += 86400
    return l_date


def json_load_from_file(filename):
    with open(filename, 'rU') as f:
        dataStr = f.read()
        # convert to json format
        dataStr_new = re.sub('([{,]\s*)([^{"\':]+)(\s*:)',  r'\1"\2"\3', dataStr)
        data = json.loads(dataStr_new)
        #print data
    return data


# get id and category relationship
def get_category_info(filename):
    category_info = {}
    data = json_load_from_file(filename)
    for category in data:
        categoryId = category['categoryId']
        hotTitle = category['hotTitle'].replace('热门'.decode('utf-8'), '')
        category_info[categoryId] = hotTitle
        print categoryId, hotTitle
    #print category_info
    return category_info


# get id and city relationship
def get_city_info(filename):
    city_info = {}
    data = json_load_from_file(filename)
    for k, v in data.iteritems():
        #print k, v
        cityId = v['id']
        city_nm = v['nm']
        city_info[cityId] = city_nm
    return city_info


#url_link_page_1 = 'https://m.dianping.com/myshow/ajax/performances/{};st=0;p=1;s=10;tft=0?cityId={}&sellChannel=7' .format(categoryId, cityId)

#url = 'https://m.dianping.com/myshow/ajax/performances/0;st=0;p=7;s=10;tft=0?cityId=10&sellChannel=7'


# request url
def get_one(url):
    try:
        random_useragent = random.choice(USERAGENT_CONFIG)
        r = requests.get(url, headers={'User-Agent': random_useragent}, verify=False)
    except:
        r = requests.get(url, headers=douban_headers, verify=False)
    finally:
        if r.status_code != 200:
            return False
        if r.text == '':
            r = requests.get(url, headers=show_header_wx, verify=False)
    return r.json()


def get_one_wx(url):
    try:
        r = requests.get(url, headers=show_header_wx, verify=False)
    finally:
        if r.status_code != 200:
            return False
    return r.json()


def post_data(payload):
    querystring = {"action":"addShows"}
    url = "https://piao-6gtumoevea8bb36a-1306331692.ap-shanghai.app.tcloudbase.com"
    # request url error
    try:
        r = requests.request("POST", url, data=payload, headers=add_headers, params=querystring, verify=False)
    except Exception, e:
        mylog.error("request url error, Exception:{}\traw_data:\t{}," .format(e, "result_dict")) 
        return False


    if r.status_code != 200:
        mylog.error("request time out {}" .format("result_dict")) 
    else:
        try:
            json_data= r.json()
            if json_data['addedCount'] == 0:
                mylog.info("already added, rsp_data:\t{}\traw_data:\t{}" .format(json_data, payload))
            else:
                mylog.info("added success, rsp_data:\t{}\traw_data:\t{}" .format(json_data, payload))
        # json_data do not have key named 'addedCount', such as {"warn":"forbidden"}
        except Exception, e:
            mylog.error("request time out, Exception:{}, rsp_data:\t{}\traw_data:\t{}" .format(e, json_data, payload)) 
        print(r.text)
        print(r.status_code)


def get_price_info(url):
    try:
        show_data = get_one_wx(url)['data']
        l_price = [ int(x['ticketPrice']) for x in show_data ]
    except Exception as e:
        print "get_price_info: {} {}" .format(url, e)
        l_price = []
    #print l_price
    return l_price


# l_startTime: ["2021-07-02 19:30", "2021-07-03 19:30", "2021-07-04 14:30"] 
# l_all_price: [100, 220, 380]
def get_shows_info(performanceId):
    #url = 'https://show.maoyan.com/maoyansh/myshow/ajax/v2/performance/{}/shows/1' .format(performanceId)
    #url = 'https://m.dianping.com/myshow/ajax/v2/performance/{}/shows/1' .format(performanceId)
    url = 'https://wx.maoyan.com/maoyansh/myshow/ajax/v2/performance/{}/shows/1' .format(performanceId)
    print "shows_url: {}" .format(url)
    l_all_price = []
    shows_data = []
    try:
        json_data = get_one_wx(url)
        shows_data = json_data['data']
    except Exception as e:
        print "exception, get_shows_info: {} {}" .format(url, e)
        l_startTime = []
        url = 'https://show.maoyan.com/maoyansh/myshow/ajax/v2/performance/{}/shows/1' .format(performanceId)
    finally:
        print "shows_data: {}" .format(shows_data)
        for show in shows_data[0:2]:
            showId = show['showId']
            #show_url = 'https://show.maoyan.com/maoyansh/myshow/ajax/v2/show/{}/tickets' .format(showId)
            #show_url = 'https://m.dianping.com/myshow/ajax/v2/show/{}/tickets' .format(showId)
            show_url = 'https://wx.maoyan.com/maoyansh/myshow/ajax/v2/show/{}/tickets' .format(showId)
            #print "show_url:{}" .format(show_url)
            show_price = get_price_info(show_url)
            for p in show_price:
                if p not in l_all_price:
                    l_all_price.append(p)
            random_sleep(1, 3)
        if len(shows_data) > 0:
            l_startTime = [ x['startTimeDateFormatted']+' '+x['startTimeTimeFormatted'] for x in shows_data ]
            #print json.dumps(l_startTime)
    return l_startTime, sorted(l_all_price)


def get_drama_base_info(url):
    # request
    drama_infos['error'] = None
    if not get_one(url):
        drama_infos['error'] = 'request error'
        return drama_infos
    json_data = get_one(url)
    drama_infos['info'] = json_data['data']
    drama_infos['totalHits'] = 0 if json_data['paging'] == None else json_data['paging']['totalHits']
    return drama_infos


def get_drama_city_info(categoryId, cityId):
    shows = []
    url_link_page_1 = 'https://m.dianping.com/myshow/ajax/performances/{};st=0;p=1;s=10;tft=0?cityId={}&sellChannel=7' .format(categoryId, cityId)
    totalHit = get_drama_base_info(url_link_page_1)['totalHits']
    print totalHit
    total_num = totalHit/10 if totalHit % 10 == 0 else totalHit/10 + 1
    print total_num
    for page in xrange(4, 5):
    #for page in xrange(1, total_num+1):
        url = 'https://m.dianping.com/myshow/ajax/performances/{};st=0;p={};s=10;tft=0?cityId={}&sellChannel=7' .format(categoryId, page, cityId)
        print "url: {}" .format(url)
        try:
            data = get_drama_base_info(url)
            if data['error'] is not None:
                drama_info = "{0}\t{1}" .format(url,data['error'])
                drama_info_list.append(drama_info)
            else:
                for show in data['info'][2:4]:
                #for show in data['info']:
                    performanceId = show['performanceId']
                    city = data_city[cityId]
                    category = data_category[categoryId]
                    name = show['name'].replace('\t', '')
                    shopName = show['shopName']
                    showTimeRange = show['showTimeRange']
                    priceRange = show['priceRange']
                    posterUrl = show['posterUrl']
                    dt_start, dt_end, msg = get_start_end_time(showTimeRange)
                    date_Range = get_date_list(dt_start, dt_end, msg)
                    try: 
                        startTimes, prices = get_shows_info(performanceId)
                    except Exception as e:
                        print "get_shows_info({}): {}" .format(performanceId, e)
                        startTimes, prices= [], []
                    info = dict(
                          name = name,
                          shopName = shopName,
                          priceRange = priceRange,
                          posterUrl = posterUrl,
                          date_Range = get_date_list(dt_start, dt_end, msg),
                          timeOptions = startTimes,
                          priceOptions = prices
                          )
                    shows.append(info)
                    drama_info = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}" \
                                .format(
                                    page, performanceId,
                                    city, category,
                                    name, shopName, showTimeRange,
                                    date_Range, priceRange, startTimes, 
                                    prices, posterUrl)
                    drama_info_list.append(drama_info)
                    random_sleep(1, 3)
        except Exception:
            drama_info = "{0}\tinternal_running_error" .format(url)
            drama_info_list.append(drama_info)
        #print drama_info_list
        sleeptime = random.uniform(0, 3)
        sleeptime = Decimal(sleeptime).quantize(Decimal('0.00'))
        time.sleep(sleeptime)
    #print (shows)
    print (json.dumps(shows))
    return shows


def get_all_drama_info():
    '''
    1 演唱会    -- up
    2 体育赛事  -- up
    3 戏曲艺术  -- up
    4 话剧/歌剧 -- up
    5 芭蕾舞蹈  -- up
    6 音乐会    -- up
    7 亲子演出
    8 其他
    9 休闲展览  -- up
    '''
    category_list = sorted([ k for k, v in data_category.iteritems() ])
    city_list = sorted([ k for k, v in data_city.iteritems() ])
    print "city_list: {}" .format(city_list)
    print "category_list: {}" .format(category_list)
    #for i in city_list[0:4]:
    for i in [10]:
    #for i in city_list:
    #for j in category_list[0:4]:
        for j in [9]:
        #for j in [1, 2, 3, 4, 5, 6, 9]:
            RESULT = {}
            RESULT['shows'] = get_drama_city_info(j, i)
            RESULT['city'] = data_city[i]
            RESULT['category'] = data_category[j]
            RESULT['appKey'] = appKey
            print (json.dumps(RESULT))
            store_to_file(f_result, **RESULT)
            post_data(json.dumps(RESULT))
    return drama_info_list

    
# create log and csv dir
if not os.path.isdir(LOGPATH):
    os.makedirs(LOGPATH, 0755)
if not os.path.isdir(CSVPATH):
    os.makedirs(CSVPATH, 0755)

if __name__ == '__main__':
    mylog = myLog()
    ts_today = int(time.time())
    date_today = _to_date(ts_today)
    CSVFILE = CSVPATH + os.sep + 'drama-{0}.csv' .format(date_today)
    f_category = 'category_info'
    f_city = 'city_info'
    f_csv = 'drama.csv'
    f_result='drama_info'
    # city: 4 北京 0 上海
    # categoryId: 0 全部 4 话剧/歌剧
    categoryId = 4
    #categoryId = 0
    cityId = 1
    drama_infos = {}
    drama_info_list = []
    appKey = "2_mvls9gege00l"
    data_category = get_category_info(f_category)
    data_city = get_city_info(f_city)
    head_instruction = "page\tperformanceId\tcity\tcategory\tname\tshopName\tshowTimeRange\tdate_Range\tpriceRange\ttimeOptions\tpriceOptions\tposterUrl"
    #drama_info_list = get_drama_city_info(categoryId, cityId)
    drama_info_list = get_all_drama_info()
    write_to_csv(CSVFILE, head_instruction, *drama_info_list)
