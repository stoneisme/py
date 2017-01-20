#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def http_get(url, params={}, header={}):
   try:
      http = requests.get(url)
      return http
   except Exception, e:
      print e   

def http_post(url, params={}, header={}):
   try:
      http = requests.post(url)
      return http
   except Exception, e:
      print e 


http = http_get('http://shop.baofeng.com/product/wirelist')

data = http.json()
i=1
for item in data:
  print i,'movieid:%d;name:%s;price:￥%s' % (int(item['movieid']), item['text'], float(item['price'])/100)
  i=i+1
