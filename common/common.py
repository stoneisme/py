#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time,datetime

class common:
   
   #时间戳转换日期格式 
   def timeToDate(self, ctime = None,fmt = "%Y-%m-%d %H:%M:%S"):
      if ctime is None:
         ctime = int(time.time())
      return time.strftime(fmt,time.localtime(ctime))
   
   #日期格式转换时间戳
   def dateToTime(self, date = None):
      fmt = '%Y-%m-%d '
      if date is None:
         return int(time.time()) 
      if date[11:13]:
         fmt += '%H'
      if date[14:16]:
         fmt += '%M'
      if date[17:19]:
         fmt += '%S'
      return int(time.mktime(time.strptime(date, fmt.strip())))
   
   #指定日期之前/后的N天N周N小时N分钟N秒日期
   def daysToDate(self, date, w = 0, d = 0, h = 0, m = 0, s = 0, fmt = "%Y-%m-%d %H:%M:%S"):
      
      (ys, ms, ds) = (0, 0, 0)
      (hs, mins, secs) = (0, 0, 0)
      
      if date[0:4]:
        ys = int(date[0:4])
      if date[5:7]:
        ms = int(date[5:7])
      if date[8:10]:
        ds = int(date[8:10])
      if date[11:13]:
        hs = int(date[11:13])
      if date[14:16]:
        mins = int(date[14:16])
      if date[17:19]:
        secs = int(date[17:19])
      d = datetime.datetime(ys, ms, ds, hs, mins, secs) + datetime.timedelta(weeks=w, days=d, hours=h, minutes=m, seconds=s)
      return d.strftime(fmt)

if __name__ == '__main__':
   print common().daysToDate(date='2016-10-28', d = 45)
   print common().dateToTime()

