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


def json_load_from_file():
    with open("movie.json", 'rU') as f:
        data = json.load(f)
        return data['data']['returnValue']


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


def get_movie_detailed_info():
    movie_info_list = []
    showScheduleMap = data['showScheduleMap']
    shows_data = get_show_info()
    cinema_name = data['cinemaVo']['cinemaName']
    for k, v in showScheduleMap.iteritems():
        movie_id = k
        movie_name = shows_data[movie_id]['showName']
        # one day
        for i in v: 
            scheduleVos = i['scheduleVos']
            showDate_list = i['dateTip'].split()[1].split('-')
            showDate = "{0}月{1}日" .format(showDate_list[0], showDate_list[1])
            # multi show in one day
            for show in scheduleVos:
                #name = show.get('showVersion', "N/A")
                name = show['showVersion'].replace(' 原版 2D', '').replace(' ', '') if '影展' in movie_name else movie_name
                beginTime = show['openTime']
                endTime = show['closeTime']
                movie_info = "{0}\t{1}\t{2}-{3}\t{4}" .format(name,showDate,beginTime,endTime,cinema_name)
                movie_info_list.append(movie_info)
                print movie_info
    return movie_info_list


if __name__ == '__main__':
    data = json_load_from_file()
    # write to movie.csv
    f_csv = 'movie.csv'
    head_instruction = "film\tdate\ttime\ttheater"
    movie_info_list = get_movie_detailed_info()
    write_to_csv(f_csv, head_instruction, *movie_info_list)
