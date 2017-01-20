#!/usr/bin/env python
#-*- coding: utf-8 -*-

#import BeautifulSoup
from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#http://www.mbaobao.com/good/search?manageId=11001,3002
#params = {"manageId":11001}

page  = 1
total =30
data  = []


def parse_category(url, params, index):
    http   = requests.get(url, params)
    Soup   = BeautifulSoup(http.text, 'lxml')
    spm_id = Soup.select('body')[0].get('data-spm')
    
    catDiv = Soup.select("#filterPanel > div:nth-of-type(%d) > ul > li > a" % index)
    data = []
    for v in catDiv:
        start = v.get('href').find("_")
        end   = v.get('href').find(".")
       	c = {'url':v.get('href'),'cat_name':v.text, 'cat_id': v.get('href')[start+1:end]}
        data.append(c)
    return spm_id, data


def parse_vidoes(url, params):
    page = 1
    data = []
    while page <= 25:
        http   = requests.get(url % page, params)

   	html   = http.text
	
   	Soup = BeautifulSoup(html,'lxml')
   	vodeos = Soup.select(".box-video .info-list li.title a")

   	for v in vodeos:
     	   data.append(v.text)
   	page = page + 1
    return data
	
url    = 'http://list.youku.com/category/video/'
spm_id, cate = parse_category(url, {}, 1)
category = {'spm_id':spm_id, 'cate': cate}
for v in category['cate']:
   spm_id,child =  parse_category('http://list.youku.com' + v['url'], {}, 2)
   for c in child:
      print "url:%s,cat_name:%s" % (c['url'],c['cat_name'])
sys.exit()
params = {'spm_id':category['spm_id'], 'cat_id':0, 'area_index':None, 'cat_index':None}
url += 'c_%s_' % params['cat_id']
if params['cat_id'] == 0:
    url += 'd_1_s_1'
url += '_p_%d.html'
spm = 'a2h1n.%s.filterPanel.5' % params['spm_id']
if params['area_index'] is not None:
   spm += '!%s' % params['area_index']
spm += '~1~3'
if params['cat_index'] is not None:
   spm += '!%s' % params['cat_index']
spm += '~A'
#url+='?spm='+spm
data = parse_vidoes(url, {'spm':spm})

for v in data:
   print v
