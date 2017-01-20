#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Create Author baihaijiang
Date 2016年12月21日
Desc 入库分类
'''

import sys
sys.path.append('..')

from common.Db import Db
from common.common import common
from common.logger import logger
import config.config as config
from common.ihttp import ihttp as http
import json


def categorylist(url):
    httpResult = http().http_get(url)
    ret = httpResult.json()
    return ret['data']

url = 'https://bshop.guanmai.cn/v587/product/category/get'
category = categorylist(url)

dbClient = Db(config.database['local'])

s = 1
for cat in category:
    sql = "INSERT INTO 91pigou_category (cat_name,cat_type,cat_desc,parent_id,sort_order,is_show) "
    sql+= "VALUES('%s', %d, '%s', %d, %d, %d) "
    
    cat['cat_id'] = dbClient.insert( sql % (cat['name'], 1, '', 0, s, 1) )
    
    s = s + 1
    s1 = 1        
    for c in cat['children']:
    	sql = "INSERT INTO 91pigou_category (cat_name,cat_type,cat_desc,parent_id,sort_order,is_show) "
        sql+= "VALUES('%s', %d, '%s', %d, %d, %d) "
    	c['cat_id'] = dbClient.insert( sql % (c['name'], 1,'', cat['cat_id'], s1, 1) )
        s1 = s1 + 1

logger('../jsons/', 'category.json').write(category)
