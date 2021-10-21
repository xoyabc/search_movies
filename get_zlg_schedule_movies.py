#!/usr/bin/env python2.7
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
import time
reload(sys)
sys.setdefaultencoding("utf-8")

import urllib3
urllib3.disable_warnings()

ticket_headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
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

def _to_timestamp(dt):
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    ts = time.mktime(timeArray)
    return ts


def _to_dt(ts):
    timeArray = time.localtime(ts)
    dt = time.strftime("%H:%M", timeArray)
    return dt


def _to_day(ts):
    timeArray = time.localtime(ts)
    day = time.strftime("%Y/%m/%d", timeArray)
    return day


def get_week_day(dt):
    week_day_dict = {
      0 : '周日',
      1 : '周一',
      2 : '周二',
      3 : '周三',
      4 : '周四',
      5 : '周五',
      6 : '周六',
    }
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    day = int(time.strftime("%w", timeArray))
    return week_day_dict[day]


def get_schedule_info(date):
    #millis = int(round(time.time() * 1000))
    cinema_url = 'https://yt.cfa.org.cn/api/movie/movieCinemaList?now={0}&cinemaName=' .format(date)
    print "cinema_url:{}" .format(cinema_url)
    res = requests.get(cinema_url, headers=ticket_headers, verify=False)
    json_data=res.json()['data']
    #print json_data
    return json_data

#sys.exit(0)


def get_movie_info(m_id):
    movie_info = {}
    movie_url = 'https://yt.cfa.org.cn/api/movie/movieInfo/{0}?userId=' .format(m_id)  
    res = requests.get(movie_url, headers=ticket_headers, verify=False)
    json_data=res.json()['data']
    # 国家/地区
    movie_info['regionCategoryName'] = "/" .join([ x['categoryName'] for x in json_data['regionCategoryNameList'] ])
    # 字幕
    movie_info['subtitle'] = '未标注' if len(json_data['subtitle']) == 0 else json_data['subtitle'][0] 
    # 版本 DCP
    movie_info['projection_material'] = 'N/A' if json_data['movieCinemaList'][0]['node'] == '' else json_data['movieCinemaList'][0]['node'].split('"')[1]
    # 画面效果
    movie_info['framesCategoryName'] = 'N/A' if json_data['framesCategoryName']  == '' else json_data['framesCategoryName']
    # 画幅比
    movie_info['frameRatio'] = 'N/A' if json_data['frameRatioList'][0] == '' else json_data['frameRatioList'][0]
    return movie_info


def get_detailed_schedule_info(schedule_data):
    for movie in schedule_data:
        movie_id = movie['movieId']
        print "movie_id:{}" .format(movie_id)
        name = movie['movieName']
        cinema_name = movie['cinemaName']
        movieHall = movie['movieHall']
        duration = movie['movieMinute']
        poster = movie['pictureLittle']
        movieActorList = movie['movieActorList']
        print "movieActorList:{0}" .format(movieActorList)
        # get all director
        director_all = "/" .join([ x['realName'].split()[0].strip() for x in movieActorList \
                   if x['position'] == '导演'.decode('utf-8') ])
        # get the first three director
        director = "/" .join(director_all.split('/')[0:3])
        movie_data = get_movie_info(movie_id)
        # get the first three country
        country = "/" .join(movie_data['regionCategoryName'].split('/')[0:3])
        print "country:{0}" .format(country)
        # get date, beginTime, endTime, week
        playTime = movie['playTime']
        showDate_list = movie['playTime'].split()[0].split('-')
        showDate = "{0}月{1}日" .format(showDate_list[1], showDate_list[2])
        beginTime = ":" .join(movie['playTime'].split()[1].split(':')[0:2])
        ts_start = _to_timestamp(playTime)
        ts_endTime = duration * 60 + ts_start
        endTime = _to_dt(ts_endTime)
        week = get_week_day(playTime)
        #movie_info = "{0}\t{1}\t{2}-{3}\t{4}\t{5}\t{6}\t{7}\t{8}" .format(name,showDate,beginTime,endTime,cinema_name,director,shot_year,country,poster)
        movie_info = "{0}\t{1}\t{2}-{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}" \
                                                             .format(name,showDate,beginTime,endTime,
                                                                     week,duration,cinema_name,movieHall,director,country,
                                                                     movie_data['subtitle'],movie_data['projection_material'],
                                                                     movie_data['frameRatio'])
        movie_info_list.append(movie_info)
        print cinema_name,duration,name,movieHall,poster,director
        print movie_info


def judge_list_dup_element(list_name, n, v=0):
    # check if continuous n elements in a list
    # `n` stand for the number of continuous element
    # `v` stand for the value of dup element
    for i in xrange(len(list_name)-n+1):
        if list_name[i] == v and len(list(set(list_name[i:i+n]))) == 1:
            return True
            break
    return False


def get_movie_detailed_info(start_day):
    ts_start_day = _to_timestamp(start_day)
    ts_end_day = ts_start_day + 31*24*60*60
    cnt = 0
    schedule_list = []
    while ts_start_day <= ts_end_day:
        date = _to_day(ts_start_day)
        schedule_data = get_schedule_info(date)
        # stop once there are no shows for 3 consecutive days
        if judge_list_dup_element(schedule_list, 3, 0):
            break
        if len(schedule_data) > 0:
            get_detailed_schedule_info(schedule_data)
            # set element to 1 if there are shows
            schedule_list.insert(cnt, 1)
        else:
            # set element to 0 if there are no shows
            schedule_list.insert(cnt, 0)
        #print (schedule_list)
        time.sleep(1 + random.randint(1, 3))  
        ts_start_day += 86400
        cnt += 1
    return movie_info_list


def get_schedule_list():
    # execute on the last 6 days of every month to get the movie schedule of next month
    ts_today = int(time.time())
    for i in xrange(6, 0, -1):
        # timestamp of tomorrow
        ts = ts_today + i * 86400
        year = _to_day(ts).split('/')[0]
        mon = _to_day(ts).split('/')[1]
        day = _to_day(ts).split('/')[-1]
        day_num = int(day)
        if day_num == 1:
            s_day = "{0}-{1}-{2} 00:00:00" .format(year, mon, day)
            movie_info_list = get_movie_detailed_info(s_day)
            write_to_csv(f_csv, head_instruction, *movie_info_list)


if __name__ == '__main__':
    movie_info_list = []
    # write to movie.csv
    f_csv = "movie.csv"
    head_instruction = "film\tdate\ttime\tweek\tduration\ttheater\tmovieHall\tdirector\tcountry\tsubtitle\tprojection_material\tframeRatio"
    #start_day = "2021-11-13 00:00:00"
    #movie_info_list = get_movie_detailed_info(start_day)
    #write_to_csv(f_csv, head_instruction, *movie_info_list)
    #sys.exit(0)
    get_schedule_list()
