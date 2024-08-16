#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# 2023/07/15: add lasting_days

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


def get_movie_info(m_id):
    movie_info = {}
    movie_url = 'http://api.guoyingjiaying.cn/filmcinema/getprogram_details_app?prorgam_id={0}&uid=1456' .format(m_id)  
    #movie_LibrryInfo_url = 'https://yt5.cfa.org.cn/v5/api/movie/movieLibrryInfo/{0}' .format(m_id)
    #movieActorList_url = 'https://yt5.cfa.org.cn/v5/api/movie/movieActorList/{0}' .format(m_id)
    res = requests.get(movie_url, headers=ticket_headers, verify=False)
    json_data=res.json()['data']
    #LibrryInfo_data = requests.get(movie_LibrryInfo_url, headers=ticket_headers, verify=False).json()['data']
    #movieActorList = requests.get(movieActorList_url, headers=ticket_headers, verify=False).json()['data']
    movieActorList = json_data['performer']
    print "movieActorList:{0}" .format(movieActorList)
    movie_info['movieId'] = json_data['id']
    movie_info['name'] = json_data['cn_name']
    movie_info['year'] = json_data['years_content']
    # 国家/地区
    movie_info['regionCategoryName'] = "/" .join([ x for x in json_data['film_area_code'].split() ])
    # 语言
    movie_info['languageCategoryName'] = "/" .join([ x for x in json_data['film_language_code'].split() ])
    # 字幕
    movie_info['subtitle'] = '未标注' if len(json_data['film_caption_code']) == 0 else "/" .join([ x for x in json_data['film_caption_code'].split() ])
    # 画幅比
    try:
        movie_info['frameRatio'] = 'N/A' if json_data['film_frameratio_code'] == '' else json_data['film_frameratio_code']
    except Exception:
        movie_info['frameRatio'] = 'N/A'
    # 版本 DCP
    try:
        movie_info['projection_material'] = 'N/A' if json_data['screens'][0]['screen_format'] == '' else json_data['screens'][0]['screen_format']
    except Exception:
        movie_info['projection_material'] = 'N/A'
    # 色彩
    movie_info['color'] = 'N/A' if json_data['film_color_code'] == '' else json_data['film_color_code']
    # duration
    movie_info['duration'] = 'N/A' if json_data['film_duration'] == '' else json_data['film_duration']
    # get all director
    director_all = 'N/A' if len(movieActorList) == 0 else "/" .join([ x['real_name'].split()[0].strip() for x in movieActorList \
               if x['position'] == '导演'.decode('utf-8') ])
    # get the first three director
    director = 'N/A' if director_all == 'N/A' or director_all == '' else "/" .join(director_all.split('/')[0:3])
    movie_info['director'] = director
    return movie_info


def get_detailed_schedule_info(movie_id):
    try:
        movie_data = get_movie_info(movie_id)
        print("movie id:{0}" .format(movie_id))
        print(movie_data)
        name = movie_data['name']
        # get the first three country
        country = "/" .join(movie_data['regionCategoryName'].split('/')[0:3])
        print "country:{0}" .format(country)
        # get the first three language
        language = "/" .join(movie_data['languageCategoryName'].split('/')[0:3])
        #print "language:{0}" .format(language)
        #movie_info = "{0}\t{1}\t{2}-{3}\t{4}\t{5}\t{6}\t{7}\t{8}" .format(name,showDate,beginTime,endTime,cinema_name,director,shot_year,country,poster)
        movie_info = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}" \
                                                         .format(movie_id,name,country,movie_data['year'],movie_data['director'],
                                                          movie_data['duration'],movie_data['color'],language,
                                                          movie_data['subtitle'],movie_data['frameRatio'])
    except Exception:
        movie_info = "{0}\tinternal_running_error" .format(movie_id)
    movie_info_list.append(movie_info)
    print movie_info


def get_movie_detailed_info(start_id, end_id):
    while start_id <= end_id:
        get_detailed_schedule_info(start_id)
        time.sleep(0 + random.randint(1, 2))  
        start_id += 1
    return movie_info_list


if __name__ == '__main__':
    movie_info_list = []
    # write to movie.csv
    BASEPATH = os.path.realpath(os.path.dirname(__file__))
    f_csv = BASEPATH + os.sep + 'movie.csv'
    head_instruction = "movie_id\tfilm\tcountry\tyear\tdirector\tduration\tcolor\tlanguage\tsubtitle\tframeRatio"
    movie_info_list = get_movie_detailed_info(2409, 2450)
    write_to_csv(f_csv, head_instruction, *movie_info_list)
