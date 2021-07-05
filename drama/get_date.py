#! /usr/bin/env python2.7
# -*- coding:utf-8 -*-
import time
import re

# dt_start 2021.7.30
# dt_end 2021.8.1

def _to_timestamp(dt):
    timeArray = time.strptime(dt, "%Y.%m.%d")   
    ts = time.mktime(timeArray)
    return ts

#t = '2021.7.30 - 2021.8.1'
#t = '2020.12.31 周四'
#t = '2020.12.31 / 12.31'
t = '2021.12.30 - 2022.01.01'

def get_start_end_time(t):
    if '-' in t:
        # 2021.7.30 - 2021.8.1
        dt_start = t.split('-')[0].strip()
        dt_end = t.split('-')[1].strip()
    elif '/' in t:
        # 2021.7.16 / 7.17
        pattern = re.compile(r'(?P<year>\d{4})\.(?P<m_start>\d{1,2})\.(?P<d_start>\d{1,2})[^0-9\.]*(?P<m_end>\d{1,2})\.(?P<d_end>\d{1,2})')
        year = pattern.search(t).group('year')
        dt_start = t.split('/')[0].strip()
        dt_end = "{0}.{1}" .format(year, t.split('/')[1].strip())
    elif '周' in t and ':' in t:
        dt_start = dt_end = t.split()[0].strip()
    else:
        dt_start = dt_end = 'N/A'
        return dt_start, dt_end, False
    return dt_start, dt_end, True


dt_start, dt_end, msg = get_start_end_time(t)

def get_date_list(s_time, e_time, flag=False):
    l_date = []
    if flag:
        ts_start = _to_timestamp(s_time)
        ts_end = _to_timestamp(e_time)
        while ts_start <= ts_end:
            timeArray = time.localtime(ts_start)
            dt_new = time.strftime("%Y年%m月%d日", timeArray)
            l_date.append(dt_new.decode('utf-8'))
            ts_start += 86400
    return l_date


print get_date_list(dt_start, dt_end, msg)
