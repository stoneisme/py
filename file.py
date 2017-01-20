#!/usr/bin/env python

try:
  f = open("https://bshop.guanmai.cn/static/productpic/7724f58181ea7bc3.jpg")
  data = f.read()
  f.close()
 
  print data
except IOError, e:
  print e 

try:
  config = open("/tmp/a.json")
  configs = eval(config.read())
  print configs;
  print configs.get("name")
  print configs.get("birthday") 
except Exception as m:
  print m 
