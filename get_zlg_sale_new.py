#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import re 
import sys 
import os
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

#ticket_headers = {
#    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
#    }

ticket_headers = {
    'user-agent': "Mozilla/5.0  AppleWebKit/537.36 Version/4.0 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/33.893127)",
    'Authori-zation': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwd2QiOiJkNDFkOGNkOThmMDBiMjA0ZTk4MDA5OThlY2Y4NDI3ZSIsImlzcyI6ImFwaS5ndW95aW5namlheWluZy5jbiIsImF1ZCI6ImFwaS5ndW95aW5namlheWluZy5jbiIsImlhdCI6MTcyMTYyNDkwNywibmJmIjoxNzIxNjI0OTA3LCJleHAiOjE3NTMxNjA5MDcsImp0aSI6eyJpZCI6MTQ1NiwidHlwZSI6ImFwaSJ9fQ.sesor14ewLKctSrqFyV1MqLACVAgiVaZ8Y66J50LliA",
    'Cookie': "cb_lang=zh-cn; PHPSESSID=ee68cbd9f743de78220e39adb8eb45da"
    }

# write to csv file
def write_to_csv(filename, head_line, *info_list):
    with open(filename, 'w') as f:
        f.write(codecs.BOM_UTF8)
        writer = csv.writer(f)
        writer.writerow(head_line.split('\t'))
        theater_order = ["百子湾艺术影院", "小西天艺术影院", "江南分馆影院"]
        hall_order = ["4号厅", "3号厅", "2号厅", "1号厅"]
        theater_order_map = {theater: index for index, theater in enumerate(theater_order)}
        hall_order_map = {hall: index for index, hall in enumerate(hall_order)}
        info_list_new = [ x.split('\t') for x in info_list]
        info_list = sorted(info_list_new, key=lambda x:(theater_order_map.get(x[4], 1), hall_order_map.get(x[5], 1), int(x[7])), reverse=True)
        for row_list in info_list:
            #row_list = row.split('\t')
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
    year = date.split('/')[0]
    month = date.split('/')[1]
    cinema_url = 'http://api.guoyingjiaying.cn/filmcinema/getcalendar?year={0}&month={1}&cinema_code=' .format(year, month)
    print "cinema_url:{}" .format(cinema_url)
    try:
        res = requests.get(cinema_url, timeout=5, headers=ticket_headers, verify=False)
        json_data = [ j for x in res.json()['data']['list'] if len(x['screen']) >0 for j in x['screen'] ]
    except requests.exceptions.RequestException as e:
        json_data = []
    #print json_data
    return json_data


def get_chinema_seat_info(screen_id, place_id):
    movie_url = 'http://api.guoyingjiaying.cn/filmcinema/getchinema_seat?screen_id={0}&place_id={1}' .format(screen_id, place_id)
    res = requests.get(movie_url, headers=ticket_headers, verify=False)
    json_data=res.json()['data']['restmap']
    return json_data


def get_movie_info(m_id, movieRewindingId):
    movie_info = {}
    movie_url = 'http://api.guoyingjiaying.cn/filmcinema/getprogram_details_app?prorgam_id={0}&uid=1456' .format(m_id)  
    res = requests.get(movie_url, headers=ticket_headers, verify=False)
    json_data=res.json()['data']
    movieActorList = json_data['performer']
    print "movieActorList:{0}" .format(movieActorList)
    # get all director
    movie_info['director_all'] = 'N/A' if len(movieActorList) == 0 else "/" .join([ x['real_name'].split()[0].strip() for x in movieActorList \
               if x['position'] == '导演'.decode('utf-8') ])
    # 国家/地区
    movie_info['regionCategoryName'] = "/" .join([ x for x in json_data['film_area_code'].split() ])
    # 语言
    movie_info['languageCategoryName'] = "/" .join([ x for x in json_data['film_language_code'].split() ])
    # 字幕
    movie_info['subtitle'] = '未标注' if len(json_data['film_caption_code']) == 0 else "/" .join([ x for x in json_data['film_caption_code'].split() ])
    # 版本 DCP
    #movie_info['projection_material'] = 'N/A' if len(json_data['film_pformat_code']) == 0 else json_data['film_pformat_code']
    movie_info['projection_material'] = 'N/A' if json_data['screens'][0]['screen_format'] == '' else json_data['screens'][0]['screen_format']
    # 画幅比
    try:
        movie_info['frameRatio'] = 'N/A' if json_data['film_frameratio_code'] == '' else json_data['film_frameratio_code']
    except Exception:
        movie_info['frameRatio'] = 'N/A'
    # get movieCinemaList data
    movieCinemaList_data = json_data['screens']
    for cinema_info in movieCinemaList_data:
        #print "cinema_info: {}" .format(cinema_info)
        info_id = cinema_info['id']
        place_id = cinema_info['place_id']
        if info_id == movieRewindingId:
            seat_data = get_chinema_seat_info(movieRewindingId, place_id)
            print "info_id {0} {1}" .format(info_id, movieRewindingId)
            print "seatTotal: {}" .format(seat_data['seat_count'])
            # 售卖情况
            movie_info['seatTotal'] = 'N/A' if seat_data['seat_count'] == '' else seat_data['seat_count']
            movie_info['seatSold'] = 'N/A' if seat_data['sold_count'] == '' else seat_data['sold_count']
    return movie_info


def get_detailed_schedule_info(schedule_data, cinema_list):
    for movie in schedule_data:
        if movie['screen_cinema'] in cinema_list:
            movie_id = movie['movie_id']
            program_id = movie['program_ids']
            movieRewindingId = movie['id']
            print "program_id:{}" .format(program_id)
            print "movieRewindingId:{}" .format(movieRewindingId)
            name = movie['show_name']
            screen_cinema = movie['screen_cinema']
            cinema_name = screen_cinema.split()[0]
            movieHall = screen_cinema.split()[1]
            duration = movie['screen_time_len']
            poster = movie['cover_img1']
            movie_data = get_movie_info(program_id, movieRewindingId)
            # get the first three director
            director = "/" .join(movie_data['director_all'].split('/')[0:3])
            # get the first three country
            country = "/" .join(movie_data['regionCategoryName'].split('/')[0:3])
            print "country:{0}" .format(country)
            # get sale info
            #seatTotal = int(movie_data['seatTotal'])
            #seatSold = int(movie_data['seatSold'])
            seatTotal = 'N/A' if movie_data['seatTotal'] == None else int(movie_data['seatTotal'])
            seatSold = 'N/A' if movie_data['seatSold'] == None else int(movie_data['seatSold'])
            sale_percent = 'N/A' if movie_data['seatTotal'] == None else '{:.0%}'.format(float(seatSold) / float(seatTotal))
            # get date, beginTime, endTime, week
            playTime = movie['screen_start_time']
            showDate_list = movie['screen_start_time'].split()[0].split('-')
            showDate = "{0}月{1}日" .format(showDate_list[1], showDate_list[2])
            beginTime = ":" .join(movie['screen_start_time'].split()[1].split(':')[0:2])
            ts_start = _to_timestamp(playTime)
            ts_endTime = duration * 60 + ts_start
            endTime = _to_dt(ts_endTime)
            week = get_week_day(playTime)
            #movie_info = "{0}\t{1}\t{2}-{3}\t{4}\t{5}\t{6}\t{7}\t{8}" .format(name,showDate,beginTime,endTime,cinema_name,director,shot_year,country,poster)
            movie_info = "{0}\t{1}\t{2}-{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}" \
                                                                 .format(name,showDate,beginTime,endTime,
                                                                         week,cinema_name,movieHall,director,
                                                                         seatSold,seatTotal,sale_percent)
            movie_info_list.append(movie_info)
            time.sleep(0 + random.randint(0, 2000)/1000) 
            print cinema_name,duration,name,movieHall,poster,director
            print movie_info


def get_movie_detailed_info(start_day, cinema='北京总馆', lasting_days=31):
    if cinema == '北京总馆':
        cinema_list = ["小西天艺术影院 2号厅", "小西天艺术影院 1号厅", "百子湾艺术影院 1号厅"]
    elif cinema == '江南分馆':
        cinema_list = ["江南分馆影院 1号厅", "江南分馆影院 4号厅"]
    else:
        cinema_list = ["小西天艺术影院 2号厅", "小西天艺术影院 1号厅", "百子湾艺术影院 1号厅", "江南分馆影院 1号厅", "江南分馆影院 4号厅"]
    ts_start_day = _to_timestamp(start_day)
    ts_end_day = ts_start_day + lasting_days*24*60*60
    month_list = []
    while ts_start_day <= ts_end_day:
        month  =  "/" .join(_to_day(ts_start_day).split('/')[0:2])
        if month not in month_list:
            schedule_data = get_schedule_info(month)
            if len(schedule_data) > 0:
                get_detailed_schedule_info(schedule_data, cinema_list)
        month_list.insert(0, month)
        ts_start_day += 86400
    return movie_info_list


def get_schedule_list():
    # execute on the last 6 days of every month to get the movie schedule of next month
    ts_today = int(time.time())
    for i in xrange(7, 0, -1):
        # timestamp of tomorrow
        ts = ts_today + i * 86400
        year = _to_day(ts).split('/')[0]
        mon = _to_day(ts).split('/')[1]
        day = _to_day(ts).split('/')[-1]
        day_num = int(day)
        if day_num == 1:
            s_day = "{0}-{1}-{2} 00:00:00" .format(year, mon, day)
            movie_info_list = get_movie_detailed_info(s_day)
            # add file suffix
            write_to_csv(f_csv+'.'+year+mon, head_instruction, *movie_info_list)


if __name__ == '__main__':
    movie_info_list = []
    # write to movie.csv
    BASEPATH = os.path.realpath(os.path.dirname(__file__))
    f_csv = BASEPATH + os.sep + 'movie.csv'
    head_instruction = "film\tdate\ttime\tweek\ttheater\tmovieHall\tdirector\tseatSold\tseatTotal\tsale_percent"
    start_day = "2024-08-01 00:00:00"
    if len(sys.argv) > 1:
        if sys.argv[1] == 'all':
            cinema_name = 'all'
        else:
            cinema_name = '江南分馆'
    else:
        cinema_name = '北京总馆'
    movie_info_list = get_movie_detailed_info(start_day, cinema_name, 31)
    write_to_csv(f_csv, head_instruction, *movie_info_list)
    sys.exit(0)
    get_schedule_list()
