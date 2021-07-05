#! /usr/bin/env python2.7
# -*- coding:utf-8 -*-
import time
import re
import json
import sys
import requests

import os
import logging
from logging.handlers import TimedRotatingFileHandler

BASEPATH = os.path.realpath(os.path.dirname(__file__))
LOGPATH = BASEPATH + os.sep + 'log'
LOGFILE = LOGPATH + os.sep + 'post_data.log'

f = "post_data"


def myLog():
    log_fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    formatter = logging.Formatter(log_fmt)
    formatter.datefmt = '%a, %d %b %Y %H:%M:%S'
    # 创建TimedRotatingFileHandler对象
    log_file_handler = TimedRotatingFileHandler(
        filename=LOGFILE, when="midnight", interval=1, backupCount=31)
    log_file_handler.suffix = "%Y-%m-%d.log"
    log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    log_file_handler.setFormatter(formatter)
    log_file_handler.setLevel(logging.DEBUG)

    # 日志标准输出
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log.addHandler(log_file_handler)
    return log


def json_load_from_file(filename):
    with open(filename, 'rU') as f:
        dataStr = f.read()
        data = json.loads(dataStr)
        print data
    return data


add_headers = {
    "content-type": "application/json",
    'authorization': "Bearer 3e64llBnvbd6542gdifkso22vvv_32uy5Mt09h",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.26 Safari/537.36",
    "host": "piao-6gtumoevea8bb36a-1306331692.ap-shanghai.app.tcloudbase.com"
}


payload = json.dumps(json_load_from_file(f))


def post_data(payload):
    querystring = {"action":"addShows"}
    url = "https://piao-6gtumoevea8bb36a-1306331692.ap-shanghai.app.tcloudbase.com"
    # request url error
    try:
        r = requests.request("POST", url, data=payload, headers=add_headers, params=querystring, verify=False)
    except Exception, e:
        mylog.error("request url error, Exception:{}\traw_data:\t{}," .format(e, "result_dict")) 
        return False


    if r.status_code != 200:
        mylog.error("request time out {}" .format("result_dict")) 
    else:
        try:
            json_data= r.json()
            if json_data['addedCount'] == 0:
                mylog.info("already added, rsp_data:\t{}\traw_data:\t{}" .format(json_data, payload))
            else:
                mylog.info("added success, rsp_data:\t{}\traw_data:\t{}" .format(json_data, payload))
        # json_data do not have key named 'addedCount', such as {"warn":"forbidden"}
        except Exception, e:
            mylog.error("request time out, Exception:{}, rsp_data:\t{}\traw_data:\t{}" .format(e, json_data, payload)) 
        print(r.text)
        print(r.status_code)


# create log dir
if not os.path.isdir(LOGPATH):
    os.makedirs(LOGPATH, 0755)
mylog = myLog()

post_data(payload)
    

#print json_load_from_file(f)
