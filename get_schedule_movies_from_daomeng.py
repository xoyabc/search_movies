#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# https://plus.dmfilm.cn/api/festival/47?_=1614272786848

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
        #dataStr = f.read().replace('mtopjsonp2(', '').replace('mtopjsonp3(', '').replace(')', '')
        dataStr = f.read()
        data = json.loads(dataStr)
        return data['data']

# get id and Name relationship
def get_show_info():
    showVos = data['intros']
    show_infos = {}
    show_info = {}
    for show in showVos:
        showId = show['id']
        showName = show['name']
        show_info['showName'] = showName
        show_infos[showId] = show_info.copy()
    return show_infos


def get_movie_info(schedule_data):
    # one day
    for i in schedule_data: 
        showDate_list = i['date'].split('-')[-2:]
        showDate = "{0}月{1}日" .format(showDate_list[0], showDate_list[1])
        cinema_name = i['theater']['name']
        movie_name = i['movie']['name']
        #name = show['showVersion'].replace(' 原版 2D', '').replace(' ', '') if '影展' in movie_name else movie_name
        name = re.sub(r'(\s+[^ ]*\s+2D|\)|\s+)', '', show['showVersion']) if re.search(pattern, movie_name) else movie_name
        beginTime = i['time']
        endTime = i['timeEnd']
        movie_info = "{0}\t{1}\t{2}-{3}\t{4}" .format(name,showDate,beginTime,endTime,cinema_name)
        movie_info_list.append(movie_info)
        print movie_info
    

def get_movie_detailed_info(All=False):
    showScheduleMap = data['schedules']
    for k, v in showScheduleMap.iteritems():
        if All:
            get_movie_info(v)
    return movie_info_list


if __name__ == '__main__':
    f = "movie.json"
    data = json_load_from_file(f)
    print data['schedules']["2021-03-02"]
    movie_info_list = []
    # 影展: '\u5f71\u5c55' 片展: '\u7247\u5c55'
    pattern=re.compile(ur'([\u5f71\u5c55]{2,}|[\u7247\u5c55]{2,})')   
    # write to movie.csv
    f_csv = 'movie.csv'
    head_instruction = "film\tdate\ttime\ttheater"
    movie_info_list = get_movie_detailed_info(All=True)
    write_to_csv(f_csv, head_instruction, *movie_info_list)
