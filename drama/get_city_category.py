#! /usr/bin/env python2.7
# -*- coding:utf-8 -*-
import time
import re
import json
import sys

f_category = 'category_info'
f_city = 'city_info'

def json_load_from_file(filename):
    with open(filename, 'rU') as f:
        dataStr = f.read()
        dataStr_new = re.sub('([{,]\s*)([^{"\':]+)(\s*:)',  r'\1"\2"\3', dataStr)
        data = json.loads(dataStr_new)
        print data
    return data


# get id and category relationship
def get_category_info(filename):
    category_info = {}
    data = json_load_from_file(filename)
    for category in data:
        categoryId = category['categoryId']
        hotTitle = category['hotTitle'].replace('热门'.decode('utf-8'), '')
        category_info[categoryId] = hotTitle
        #hotTitle = category['hotTitle']
        print categoryId, hotTitle
    print category_info
    return category_info


# get id and city relationship
def get_city_info(filename):
    city_info = {}
    data = json_load_from_file(filename)
    for k, v in data.iteritems():
        print k, v
        cityId = v['id']
        city_nm = v['nm']
        city_info[cityId] = city_nm
    return city_info

data_category = get_category_info(f_category)
category_list = sorted([ k for k, v in data_category.iteritems()])
print category_list

data_city = get_city_info(f_city)
city_list = sorted([ k for k, v in data_city.iteritems() ])
print city_list

sys.exit(0)

for k, v in data_category.iteritems():
    print k

data_city = get_city_info(f_city)
for k, v in data_city.iteritems():
    print k, v
