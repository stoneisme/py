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


def parseGoodsList(url):
    httpResult = http().http_get(url)
    ret = httpResult.json()
    return ret['data']

def insertGoods(data,cat_id):
    dbClient = Db(config.database['local'])
    for goods in data:
        sql = 'INSERT INTO 91pigou_goods (cat_id,goods_name,goods_price,goods_unit,goods_ratio,goods_img,goods_desc,add_time)'
        sql+= ' VALUES ("%s","%s","%s","%s","%d","%s","%s","%s")'
        goods_id = dbClient.insert( sql % (cat_id,goods['name'],round(float(goods['std_sale_price'])/100,2),goods['std_unit_name'],1,'','', common().dateToTime()))
        for g in goods['skus']:
            sql = 'INSERT INTO 91pigou_goods_skus (goods_id,sku_name,sku_price,sku_unit,sku_ratio,sku_img,sku_desc,add_time)'
            sql+= ' VALUES (%d,"%s","%s","%s","%s","%s","%s","%s")'
            dbClient.insert( sql % (goods_id,g['name'],round(float(g['sale_price'])/100),g['sale_unit_name'],g['sale_ratio'],'',g['desc'], common().dateToTime()))

    	
category = logger('../jsons/', 'category.json').load()

for cat in category:
    for c in cat['children']:
       url = 'https://bshop.guanmai.cn/v587/product/sku/get?level=2&category_id=%s'
       goodslist = parseGoodsList(url % c['id'])
       insertGoods(goodslist, c['cat_id'])
