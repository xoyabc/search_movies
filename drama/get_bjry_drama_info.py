#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 北京人艺演出信息

from get_drama_info import *
from urllib import quote_plus, unquote    

url = 'http://wetix.bjry.com/wetix/bjry/api/wx_c_query_events2.html?nodecode=bjry&openid=oNgtk5yfPJMvv69rz1GmsV9y15TQ&keywords=&cityid=&category=&venues=&take=50&skip=0&page=1&pageSize=50'
show_base_url = 'http://wetix.bjry.com/wetix/bjry/api/wx_c_fetch_events_by_name.html?nodecode=bjry&openid=oNgtk5yfPJMvv69rz1GmsV9y15TQ&keywords='



def get_shows_info(url):
    l_all_price = []
    l_startTime = []
    try:
        shows_data = get_one(url)['events']
    except Exception as e:
        print "exception, get_shows_info: {} {}" .format(url, e)
    finally:
        # get price from the first two show
        for show in shows_data[0:2]:
            show_price = [ int(x) for x in show['prices'].split(",") ]
            #print show_price
            for p in show_price:
                if p not in l_all_price:
                    l_all_price.append(p)
        # get all startTime
        if len(shows_data) > 0:
            l_startTime = [ x['eventtime'] for x in shows_data ]
    return l_startTime, sorted(l_all_price)


def get_drama_base_info(url):
    # request
    drama_infos['error'] = None
    if not get_one(url):
        drama_infos['error'] = 'request error'
        return drama_infos
    json_data = get_one(url)
    drama_infos['info'] = json_data['events']
    return drama_infos


def get_drama_city_info():
    shows = []
    try:
        data = get_drama_base_info(url)
        if data['error'] is not None:
            drama_info = "{0}\t{1}" .format(url,data['error'])
            drama_info_list.append(drama_info)
        else:
            for event in data['info']:
                name = event['eventname']
                show_url = show_base_url + '{}'.format(quote_plus(name.encode('utf-8')))
                shopName = event['venuename']
                posterUrl = event['img_m']
                priceRange = "{}-{}" .format(event['prices'].split(",")[0], event['prices'].split(",")[-1])
                try:
                    startTimes, prices = get_shows_info(show_url)
                except Exception as e:
                    print "get_shows_info({}): {}" .format(show_url, e)
                    startTimes, prices= [], []
                info = dict(
                      name = name,
                      shopName = shopName,
                      priceRange = priceRange,
                      posterUrl = posterUrl,
                      timeOptions = startTimes,
                      priceOptions = prices
                      )
                drama_info = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}" \
                            .format(
                                city, category,
                                name, shopName,
                                startTimes,
                                prices, posterUrl)
                shows.append(info)
                print name,shopName,posterUrl,startTimes,prices
                drama_info_list.append(drama_info)
    except Exception:
        drama_info = "{0}\tinternal_running_error" .format(url)
        drama_info_list.append(drama_info)
    #print drama_info_list
    print (json.dumps(shows))
    return shows


def get_all_drama_info():
    appKey = "2_mvls9gege00l"
    RESULT = {}
    RESULT['shows'] = get_drama_city_info()
    RESULT['city'] = city
    RESULT['category'] = category
    RESULT['appKey'] = appKey
    print (json.dumps(RESULT))
    post_data(json.dumps(RESULT))
    return drama_info_list

mylog = myLog()

if __name__ == '__main__':
    city = '北京'
    category = '话剧/歌剧'
    f_csv = 'drama.csv'
    drama_infos = {}
    drama_info_list = []
    head_instruction = "city\tcategory\tname\tshopName\ttimeOptions\tpriceOptions\tposterUrl"
    drama_info_list = get_all_drama_info()
    write_to_csv(f_csv, head_instruction, *drama_info_list)
