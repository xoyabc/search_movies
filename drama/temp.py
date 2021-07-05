#! /usr/bin/env python2.7
# -*- coding:utf-8 -*-
import time
import re
import json
import sys
import requests
import random
from headers_config import USERAGENT_CONFIG


#performance_Id = '171105'
#url = 'https://show.maoyan.com/maoyansh/myshow/ajax/v2/performance/{}/shows/1' .format(performance_Id)


def get_one(url):
    try:
        random_useragent = random.choice(USERAGENT_CONFIG)
        r = requests.get(url, headers={'User-Agent': random_useragent} ,verify=False)
    except:
        r = requests.get(url, headers=douban_headers ,verify=False)
    finally:
        if r.status_code != 200:
            return False
    return r.json()


def random_sleep(s, e):
    sleeptime = random.uniform(s, e)
    sleeptime = Decimal(sleeptime).quantize(Decimal('0.00'))
    time.sleep(sleeptime)


def get_price_info(url):
    try:
        show_data = get_one(url)['data']
        l_price = [ int(x['ticketPrice']) for x in show_data ]
    except Exception as e:
        l_price = []
    #print l_price
    return l_price


def get_shows_info(performanceId):
    url = 'https://show.maoyan.com/maoyansh/myshow/ajax/v2/performance/{}/shows/1' .format(performanceId)
    l_all_price = []
    try:
        json_data = get_one(url)
        shows_data = json_data['data']
    except Exception as e:
        print e
        l_startTime = []
        random_sleep(0, 3)
        json_data = get_one(url)
        shows_data = json_data['data']
    finally:
        for show in shows_data:
            showId = show['showId']
            show_url = 'https://show.maoyan.com/maoyansh/myshow/ajax/v2/show/{}/tickets' .format(showId)
            #print "show_url:{}" .format(show_url)
            show_price = get_price_info(show_url)
            for p in show_price:
                if p not in l_all_price:
                    l_all_price.append(p)
        if len(json_data['data']) > 0:
            l_startTime = [ x['startTimeDateFormatted']+' '+x['startTimeTimeFormatted'] for x in json_data['data'] ]
            #print json.dumps(l_startTime)
    return l_startTime, sorted(l_all_price)
    

startTime, price = get_shows_info(171105)
print startTime, price
sys.exit(0)
