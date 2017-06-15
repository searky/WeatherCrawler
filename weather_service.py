#!/usr/bin/env python
#coding:utf-8

import urllib2
import json
import time
import sched
import sys
import MySQLdb

schedule = sched.scheduler(time.time, time.sleep)
db = MySQLdb.connect('localhost', 'username', 'password', 'db_name')
cursor = db.cursor()

# check if the wcode is in the table
def check_wcode(code, name):
    sql = "SELECT * FROM weather_wcode WHERE code='%s'" % code
    dataset = cursor.execute(sql)
    if dataset == 0:
        sql = "INSERT INTO weather_wcode(code, name) VALUES('%s', '%s')" % (code, name)
        cursor.execute(sql)
        db.commit()

# insert the weather recod to data table
def insert_item(jsonobj):
    current_date = time.strftime("%Y-%m-%d", time.localtime())

    sql = "SELECT * FROM weather_items WHERE udate='%s' AND utime='%s'" % (current_date, jsonobj['time'])
    result = cursor.execute(sql)
    if result == 0:
        pos = jsonobj['SD'].find('%')
        humidity = int(jsonobj['SD'][:pos])
        sql = "INSERT INTO weather_items(cityid, weather, temp, humidity, wd, ws, rain, aqi, udate, utime) VALUES(%d, '%s', %d, %d, '%s', '%s', %d, %d, current_date(), '%s')" % (int(jsonobj['city']), jsonobj['weathercode'], int(jsonobj['temp']), humidity, jsonobj['WD'], jsonobj['WS'], float(jsonobj['rain']), int(jsonobj['aqi']), jsonobj['time'])
        result = cursor.execute(sql)
        db.commit()

# get weather information from weather.com.cn
def getWeatherInfo():
    request = urllib2.Request("http://d1.weather.com.cn/sk_2d/101070201.html")
    request.add_header('Referer', 'http://www.weather.com.cn/weather1d/101070201.shtml')

    res = urllib2.urlopen(request)
    jscode = res.read()

    pos = jscode.find('{')
    jsoncode = jscode[pos:]
    jsonobj = json.loads(jsoncode, encoding="UTF-8")

    check_wcode(jsonobj['weathercode'], jsonobj['weather'])
    insert_item(jsonobj)

def performAction():
    try:
        getWeatherInfo()
    except Exception as e:
        print e

    # get weather information each 300 seconds(5 minutes)
    schedule.enter(300, 0, performAction, ())

def scheduleFunc():
    schedule.enter(1, 0, performAction, ())
    print "Starting weather crawler...\n"
    schedule.run()

scheduleFunc()