#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import re 
import sys 
import requests
import json
import csv
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")

import urllib3
urllib3.disable_warnings()

'''
https://wxapi.m.taopiaopiao.com/h5/mtop.film.mtopscheduleapi.getcinemaschedules/7.0/?jsv=2.6.1&appKey=12574478&t=1607999868430&sign=23afd6f97fa4ed72331c912ee726b1a3&api=mtop.film.MtopScheduleAPI.getCinemaSchedules&v=7.0&timeout=10000&forceAntiCreep=true&AntiCreep=true&type=jsonp&dataType=jsonp&callback=mtopjsonp2&data=%7B%22cinemaId%22%3A%2243843%22%2C%22h5AccessFlag%22%3A1%2C%22isMovieDate%22%3A0%2C%22platform%22%3A%2242%22%7D
'''

# write to csv file
def write_to_csv(filename, head_line, *info_list):
    with open(filename, 'w') as f:
        f.write(codecs.BOM_UTF8)
        writer = csv.writer(f)
        writer.writerow(head_line.split('\t'))
        for row in info_list:
            row_list = row.split('\t')
            writer.writerow(row_list)


# convert to json format
def json_load_from_file(filename):
    with open(filename, 'rU') as f:
        dataStr = f.read().replace('mtopjsonp1(', '').replace('mtopjsonp2(', '').replace('mtopjsonp3(', '')
        # remove last ")"
        dataStr_new = re.sub(r'\)$', r'', dataStr)
        data = json.loads(dataStr_new)
        return data['data']['returnValue']


# get id and Name relationship
def get_show_info():
    showVos = data['showVos']
    show_infos = {}
    show_info = {}
    for show in showVos:
        showId = show['showId']
        showName = show['showName']
        show_info['showName'] = showName
        show_infos[showId] = show_info.copy()
    return show_infos


def get_movie_info(schedule_data,cinema_name):
    # one day
    for i in schedule_data: 
        scheduleVos = i['scheduleVos']
        showDate_list = i['dateTip'].split()[1].split('-')
        showDate = "{0}月{1}日" .format(showDate_list[0], showDate_list[1])
        # multi show in one day
        for show in scheduleVos:
            #name = show['showVersion'].replace(' 原版 2D', '').replace(' ', '') if '影展' in movie_name else movie_name
            # remove ' 原版 2D' and ' 原版2D'
            name = re.sub(r'(\s+[^ ]*\s*2D|\)|\s+)', '', show['showVersion']) if re.search(pattern, movie_name) else movie_name
            beginTime = show['openTime']
            endTime = show['closeTime']
            hallName = show['hallName']
            oriPrice = show['oriPrice']
            Price = int(oriPrice)/100
            movie_info = "{0}\t{1}\t{2}-{3}\t{4}\t{5}\t{6}" .format(name,showDate,beginTime,endTime,cinema_name,hallName,Price)
            movie_info_list.append(movie_info)
            print movie_info
    

def get_movie_detailed_info(All=False):
    global movie_name
    showScheduleMap = data['showScheduleMap']
    shows_data = get_show_info()
    cinema_name = data['cinemaVo']['cinemaName']
    for k, v in showScheduleMap.iteritems():
        movie_id = k
        try:
            movie_name = shows_data[movie_id]['showName']
        except Exception as e:
            pass
        if All:
            get_movie_info(v, cinema_name)
        else:
            #if '影展' in movie_name or '片展' in movie_name:
            if re.search(pattern, movie_name):
                get_movie_info(v, cinema_name)
    return movie_info_list


if __name__ == '__main__':
    f = "movie.json"
    data = json_load_from_file(f)
    cinema_id = data['cinemaVo']['cinemaId']
    movie_info_list = []
    # 影展: '\u5f71\u5c55' 片展: '\u7247\u5c55'
    #pattern=re.compile(ur'([\u5f71\u5c55]{2,}|[\u7247\u5c55]{2,})')   
    # 匹配各类影展标题
    # 电影展/影像展 新片展 大师展 电影周  作品展  纪念展 电影季 回顾展 
    # 专题展 特展 特别放映 纪念专场 修复展 电影节 展映/展映周
    # ([影片师特题展]|作品|纪念|回顾|修复){1,}.*?([展周季节映]|专场|放映){1,}
    pattern=re.compile(ur'([\u5f71\u7247\u5e08\u7279\u9898\u5c55]|\u4f5c\u54c1|\u7eaa\u5ff5|\u56de\u987e|\u4fee\u590d){1,}.*?([\u5c55\u5468\u5b63\u8282\u6620]|\u4e13\u573a|\u653e\u6620){1,}')
    # write to movie.csv
    f_csv = 'movie.csv'
    head_instruction = "film\tdate\ttime\ttheater\thallName\tPrice"
    if len(sys.argv) > 1:
        if sys.argv[1] == 'all':
            movie_info_list = get_movie_detailed_info(All=True)
    else:
        # 资料馆小西天、百子湾店获取所有排片
        if cinema_id in ['45797', '45798']:
            movie_info_list = get_movie_detailed_info(All=True)
        # 其他影院获取影展排片
        else:
            movie_info_list = get_movie_detailed_info()
    write_to_csv(f_csv, head_instruction, *movie_info_list)
