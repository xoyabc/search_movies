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

cinemas_url = [
'http://group.leying.com/cinema/play-info?.sig=f481dd04ced792236d7cfd6d3788a683&cinema_id=12&city_id=499&client_id=00e02cf9a0191&group=10000&pver=7.0&session_id=5fcdc6b368629ebe73094539eaf19bb56675b8f6d0a5a&source=105001&ver=5.9.9&width=270',
'http://group.leying.com/cinema/play-info?.sig=45af657165af48c082f067e021cd868d&cinema_id=13&city_id=499&client_id=00e02cf9a0191&group=10000&pver=7.0&session_id=5fcdc6b368629ebe73094539eaf19bb56675b8f6d0a5a&source=105001&ver=5.9.9&width=270'
]

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


def get_schedule_info(schedule_url):
    res = requests.get(schedule_url, headers=ticket_headers, verify=False)
    json_data=res.json()
    return json_data


def get_movie_detailed_info():
    movie_info_list = []
    for cinema_url in cinemas_url:
        schedule_data = get_schedule_info(cinema_url)
        cinema_name = schedule_data['data']['cinema_data']['name']
        schedule_movies = schedule_data['data']['movie_data']
        for movie in schedule_movies:
            duration = movie['duration']
            name = movie['movie_name']
            desc = movie['movie_desc']
            shows = movie['shows']
            for k, v in shows.iteritems():
                for show in v:
                    beginTime = show['start_time']
                    endTime = show['end_time']
                    showDate_list = k.split('-')               
                    showDate = "{0}月{1}日" .format(showDate_list[1], showDate_list[2])
                    movie_info = "{0}\t{1}\t{2}-{3}\t{4}\t{5}" \
                                 .format(name,showDate,beginTime,endTime,cinema_name,desc)
                    movie_info_list.append(movie_info)
                    print movie_info
            time.sleep(1 + random.randint(1, 3))
    return movie_info_list


if __name__ == '__main__':
    # write to movie.csv
    f_csv = 'movie.csv'
    head_instruction = "film\tdate\ttime\ttheater\tdesc"
    movie_info_list = get_movie_detailed_info()
    write_to_csv(f_csv, head_instruction, *movie_info_list)
