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

# 12 北京百老汇影城（东方新天地店）
'''
'https://group.leying.com/cinema/play-info?cinema_id=12&city_id=499&client_id=&group=10000&pver=7.0&session_id=&source=4&ver=6.5.0&width=500&.sig=4a9dd5d5daf96e24070e56871e52cbe6',
'''
# 13 北京百老汇电影中心（万国城店）
'''
'https://group.leying.com/cinema/play-info?cinema_id=13&city_id=499&client_id=&group=10000&pver=7.0&session_id=&source=4&ver=6.5.0&width=500&.sig=10100db52e33ef503e4c5aa9f0a50a7e',
'''
# 14 北京百老汇影城（LUXE全景声国瑞购物中心店）
'''
'https://group.leying.com/cinema/play-info?cinema_id=14&city_id=499&client_id=&group=10000&pver=7.0&session_id=&source=4&ver=6.5.0&width=500&.sig=50d588125eb7e33b9e472e17305a92a4',
'''
# 15 北京百老汇影城（apm店）
'''
'https://group.leying.com/cinema/play-info?cinema_id=15&city_id=499&client_id=&group=10000&pver=7.0&session_id=&source=4&ver=6.5.0&width=500&.sig=5256150418fcf0d30b8b639e538700db',
'''
# 25 北京百丽宫影城（国贸店）
'''
'https://group.leying.com/cinema/play-info?cinema_id=25&city_id=499&client_id=&group=10000&pver=7.0&session_id=&source=4&ver=6.5.0&width=500&.sig=9cd3e57db9058a659936c6d3abbc6fc1',
'''

cinemas_url = [
<<<<<<< HEAD
'https://group.leying.com/cinema/play-info?cinema_id=13&city_id=499&client_id=&group=10000&pver=7.0&session_id=&source=4&ver=6.5.0&width=500&.sig=10100db52e33ef503e4c5aa9f0a50a7e',
'https://group.leying.com/cinema/play-info?cinema_id=15&city_id=499&client_id=&group=10000&pver=7.0&session_id=&source=4&ver=6.5.0&width=500&.sig=5256150418fcf0d30b8b639e538700db'
=======
'https://group.leying.com/cinema/play-info?cinema_id=13&city_id=499&client_id=&group=10000&pver=7.0&session_id=&source=4&ver=6.5.0&width=500&.sig=10100db52e33ef503e4c5aa9f0a50a7e'
>>>>>>> 5b8c6037e855c2ca623fc0ffabc2f53be7d242d7
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
            shows = movie['shows']
            for k, v in shows.iteritems():
                for show in v:
                    beginTime = show['start_time']
                    endTime = show['end_time']
                    showDate_list = k.split('-')               
                    showDate = "{0}月{1}日" .format(showDate_list[1], showDate_list[2])
                    movie_info = "{0}\t{1}\t{2}-{3}\t{4}" \
                                 .format(name,showDate,beginTime,endTime,cinema_name)
                    movie_info_list.append(movie_info)
                    print movie_info
        time.sleep(1 + random.randint(1, 3))
    return movie_info_list


if __name__ == '__main__':
    # write to movie.csv
    f_csv = 'movie.csv'
    head_instruction = "film\tdate\ttime\ttheater"
    movie_info_list = get_movie_detailed_info()
    write_to_csv(f_csv, head_instruction, *movie_info_list)
