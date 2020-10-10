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

cinemas = [65567]

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


def get_schedule_info(cinema_id):
    millis = int(round(time.time() * 1000))
    base_url = 'https://ticket.nexttix.net/api/cinemas/' 
    cinema_url = '{0}{1}?_={2}' .format(base_url,cinema_id,millis)  
    print cinema_url
    res = requests.get(cinema_url, headers=ticket_headers, verify=False)
    json_data=res.json()
    return json_data


def get_movie_info(m_id):
    millis = int(round(time.time() * 1000))
    base_url = 'https://ticket.nexttix.net/api/movies/' 
    movie_url = '{0}{1}?_={2}' .format(base_url,m_id,millis)  
    print movie_url
    res = requests.get(movie_url, headers=ticket_headers, verify=False)
    json_data=res.json()
    return json_data


def get_movie_detailed_info():
    movie_info_list = []
    for cinema_id in cinemas:
        schedule_data = get_schedule_info(cinema_id)
        cinema_name = schedule_data['data']['name']
        schedule_movies = schedule_data['data']['movies']
        for movie in schedule_movies:
            duration = movie['duration']
            #name = movie['name']
            poster = movie['poster']
            director = movie['director'].replace(', ','/')
            shows = movie['shows']
            movie_id = movie['id']
            movie_data = get_movie_info(movie_id)
            shot_year = 'N/A' if movie_data['data']['date'] == '' else movie_data['data'].get('date', 'N/A').split('-')[0]
            country = 'N/A' if movie_data['data']['country'] == '' else movie_data['data'].get('country', 'N/A').replace(', ','/')
            #print shows
            for k, v in shows.iteritems():
                for show in v:
                    name = show['version']
                    beginTime = show['beginTime']
                    endTime = show['endTime']
                    showDate = show['showDate'].replace('-','/')
                    movie_info = "{0}\t{1}\t{2}-{3}\t{4}\t{5}\t{6}\t{7}\t{8}" .format(name,showDate,beginTime,endTime,cinema_name,director,shot_year,country,poster)
                    movie_info_list.append(movie_info)
                    print movie_info
            #sys.exit(0)
            #print cinema_name,duration,name,poster,director
            time.sleep(1 + random.randint(1, 3))  
    return movie_info_list

if __name__ == '__main__':
    # write to movie.csv
    f_csv = 'movie.csv'
    head_instruction = "film\tdate\ttime\ttheater\tdirector\tshot_year\tcountry\tposter"
    movie_info_list = get_movie_detailed_info()
    write_to_csv(f_csv, head_instruction, *movie_info_list)
