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
from headers_config import HEADER_CONFIG
reload(sys)
sys.setdefaultencoding("utf-8")

import urllib3
urllib3.disable_warnings()

#ticket_headers = {
#    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
#    }

ticket_headers = {
    'user-agent': "Mozilla/5.0  AppleWebKit/537.36 Version/4.0 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/33.893127)",
    'Authori-zation': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwd2QiOiJkNDFkOGNkOThmMDBiMjA0ZTk4MDA5OThlY2Y4NDI3ZSIsImlzcyI6ImFwaS5ndW95aW5namlheWluZy5jbiIsImF1ZCI6ImFwaS5ndW95aW5namlheWluZy5jbiIsImlhdCI6MTcyNjI3NDcyMiwibmJmIjoxNzI2Mjc0NzIyLCJleHAiOjE3NTc4MTA3MjIsImp0aSI6eyJpZCI6ODE2MzIsInR5cGUiOiJhcGkifX0.BSkVFG_TjxY2649C0YVnw-eM2soaQvH6b0VpQ-_zkc8",
    'Cookie': "cb_lang=zh-cn; PHPSESSID=ee68cbd9f743de78220e39adb8eb45da"
    }
ticket_headers['Authori-zation'] = HEADER_CONFIG['Authori-zation']
ticket_headers['Cookie'] = HEADER_CONFIG['Cookie']

# 请求参数
payload = {
    'program_id': '1003',
    'uid': 86265
    }

# write to csv file
def write_to_csv(filename, head_line, *info_list):
    name_list = []
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            #for x in f:
            #    print len(x.split(','))
            #    if len(x.split(',')) > 1:
            #        name_list.append(x.split(',')[2]) 
            #name_list = [ x.split(',')[2] for x in f if len(x.split(',')) > 1 ]
            name_list = [ x.split(',')[2] for x in f if len(x.split(',')) > 1 ]
            #print name_list
    with open(filename, 'a+') as f:
        f.write(codecs.BOM_UTF8)
        writer = csv.writer(f)
        file_size = os.path.getsize(filename)
        if not file_size > 0:
            writer.writerow(head_line.split('\t'))
        for row in info_list:
            name = row.split('\t')[2]
            print "name:{0}" .format(name)
            if not name in name_list:
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
    day = time.strftime("%Y-%m-%d", timeArray)
    return day


def _to_mon(ts):
    timeArray = time.localtime(ts)
    mon = time.strftime("%Y-%m", timeArray)
    return mon


def get_movie_info(m_id):
    movie_info = {}
    payload['program_id'] = m_id
    movie_url = 'https://api.guoyingjiaying.cn/api/v3/movie/getProgramDetailsApp'
    #movie_url = 'https://api.guoyingjiaying.cn/filmcinema/getprogram_details_app?prorgam_id={0}&uid=81632' .format(m_id)  
    #movie_LibrryInfo_url = 'https://yt5.cfa.org.cn/v5/api/movie/movieLibrryInfo/{0}' .format(m_id)
    #movieActorList_url = 'https://yt5.cfa.org.cn/v5/api/movie/movieActorList/{0}' .format(m_id)
    #res = requests.get(movie_url, headers=ticket_headers, verify=False)
    res = requests.request("POST", movie_url, data=payload, headers=ticket_headers)
    json_data=res.json()['data']
    #LibrryInfo_data = requests.get(movie_LibrryInfo_url, headers=ticket_headers, verify=False).json()['data']
    #movieActorList = requests.get(movieActorList_url, headers=ticket_headers, verify=False).json()['data']
    movieActorList = json_data['performer']
    #print "movieActorList:{0}" .format(movieActorList)
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
        movie_info['frameRatio'] = 'N/A' if json_data['film_frameratio_code'] == '' else json_data['film_frameratio_code'].strip()
    except Exception:
        movie_info['frameRatio'] = 'N/A'
    # 版本 DCP
    try:
        movie_info['projection_material'] = 'N/A' if json_data['screens'][0]['screen_format'] == '' else json_data['screens'][0]['screen_format'].strip()
    except Exception:
        movie_info['projection_material'] = 'N/A'
    # 色彩
    movie_info['color'] = 'N/A' if json_data['film_color_code'] == '' else json_data['film_color_code'].strip()
    # duration
    movie_info['duration'] = 'N/A' if json_data['film_duration'] == '' else json_data['film_duration']
    # get all director
    director_all = 'N/A' if len(movieActorList) == 0 else "/" .join([ x['real_name'].split()[0].strip() for x in movieActorList \
               if x['position'] == '导演'.decode('utf-8') ])
    # get the first three director
    director = 'N/A' if director_all == 'N/A' or director_all == '' else "/" .join(director_all.split('/')[0:3])
    movie_info['director'] = director
    # get create_time
    movie_info['createTime'] = json_data['create_time'].split()[0].strip()
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
        movie_info = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}" \
                                                         .format(movie_data['createTime'],
                                                          movie_id,name,country,movie_data['year'],movie_data['director'],
                                                          movie_data['duration'],movie_data['color'],language,
                                                          movie_data['subtitle'],movie_data['frameRatio'])
    except Exception:
        movie_info = "{0}\tinternal_running_error" .format(movie_id)
    movie_info_list.append(movie_info)
    print movie_info


def get_movie_detailed_info(today):
    # get_movie_program_id
    name_payload = {'cn_name': '共同的语言'}
    movie_url = "https://api.guoyingjiaying.cn/api/v3/movie/searchMovie"
    program_ids = []
    picture_originals = []
    with open("zlg_dict.txt", "r") as f:
        # 逐行遍历
        for line in f:
            # 去除每行末尾的换行符（可选）
            line = line.strip()
            #print line
            # 处理每行内容
            name_payload['cn_name'] = line
            res = requests.request("POST", movie_url, json=name_payload, headers=ticket_headers)
            try:
                json_data = res.json()['data']
                if json_data['list'] > 0:
                    for x in json_data['list']:
                        if today in x['create_time'] and not x['picture_original'] in picture_originals:
                            program_ids.append(x['id'])
                            picture_originals.append(x['picture_original'])
            except Exception:
                pass
            time.sleep(random.randint(3, 5))
    for id in program_ids:
        get_detailed_schedule_info(id)
        time.sleep(3 + random.randint(0, 3))
    return movie_info_list


if __name__ == '__main__':
    movie_info_list = []
    cur_ts = int(time.time())
    mon = _to_mon(cur_ts)
    # write to movie.csv
    BASEPATH = os.path.realpath(os.path.dirname(__file__))
    f_csv = BASEPATH + os.sep + 'movie-' + mon + '.csv'
    head_instruction = "createTime\tmovie_id\tfilm\tcountry\tyear\tdirector\tduration\tcolor\tlanguage\tsubtitle\tframeRatio"
    today = _to_day(cur_ts)
    #today = '2025-09'
    movie_info_list = get_movie_detailed_info(today)
    write_to_csv(f_csv, head_instruction, *movie_info_list)
