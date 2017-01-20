#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
sys.path.append('..')

from common.logger import logger
import requests, json, xlwt


def http_post(url, params={}, header={}):
   try:
      http = requests.post(url, params)
      return http
   except Exception, e:
      print e


params = {}
params['platf'] = 'android'
params['mtype']  = 'normal'

turing = logger('../jsons/', 'turing.json').load()

extra  = logger('../jsons/', 'extra.json').load()

grade  = logger('../jsons/', 'grade.json').load()

httpUrl = 'http://i.turing.shouji.baofeng.com/cgi/album/details'

for g in grade:
    g = 37	
    excel = xlwt.Workbook()  # 创建EXCEL对象

    rows  = 0
    sheet = 1

    ex = excel.add_sheet(('grade_%s_sheet_%s') % (g, sheet))  # 增加sheet对象

    ex.write(rows, 0, str('地域编号').decode('utf-8'))
    ex.write(rows, 1, str('渠道名称').decode('utf-8'))
    ex.write(rows, 2, str('渠道编号').decode('utf-8'))
    ex.write(rows, 3, str('专辑编号').decode('utf-8'))
    ex.write(rows, 4, str('在线编号').decode('utf-8'))
    ex.write(rows, 5, str('站点名称').decode('utf-8'))
    ex.write(rows, 6, str('开关').decode('utf-8'))

    rows = rows + 1

    params['grade'] = g

    albumIds = turing.keys()

    record = len(albumIds)

    offset = 0
    limit = 2000

    while (offset < record):

        s = offset
        e = offset + limit
        offset = offset + limit

        aids = []

        if (e > record):
            aids = albumIds[s:]
        else:
            aids = albumIds[s:e]
        params['albums'] = {}
        params['aids'] = ",".join(str(kk) for kk in aids)

        albums = {}
        extras  = {}

        for t in aids:
            albums[t] = {}
            albums[t] = turing[t]
            if extra[t] is not None:
                extras[t] = {}
                extras[t] = extra[t]


        params['albums'] = json.dumps(albums)
        params['extra']  = json.dumps(extras)

        httpResult = http_post(httpUrl, params)

        try:

            data = httpResult.json()

            if data['status'] == 1:
                index = 0
                result = {}
                for ret in data['result'].items():

                    if len(ret[1]['turing_mode']) > 0:
                        for m in ret[1]['turing_mode'].items():
                            result[index] = {}
                            result[index]['zgid'] = str(grade[g]['zgid'])
                            result[index]['name'] = grade[g]['name']
                            result[index]['grade'] = str(g)
                            result[index]['aid'] = str(ret[1]['id'])
                            result[index]['box_mid'] = str(albums[ret[1]['id']]['box_mid'])
                            result[index]['site'] = m[1]['site']
                            result[index]['switches'] = m[1]['switches']
                            index = index + 1
                    else:
                        result[index] = {}
                        result[index]['zgid'] = str(grade[g]['zgid'])
                        result[index]['name'] = grade[g]['name']
                        result[index]['grade'] = str(g)
                        result[index]['aid'] = str(ret[1]['id'])
                        result[index]['box_mid'] = str(albums[ret[1]['id']]['box_mid'])
                        result[index]['site'] = ''
                        result[index]['switches'] = 0
                        index = index + 1


                for r in result.items():
                    if rows > 65534:
                        rows = 0
                        sheet = sheet + 1
                        ex = excel.add_sheet(('grade_%s_sheet_%s') % (g, sheet))  # 增加sheet对象

                        ex.write(rows, 0, str('地域编号').decode('utf-8'))
                        ex.write(rows, 1, str('渠道名称').decode('utf-8'))
                        ex.write(rows, 2, str('渠道编号').decode('utf-8'))
                        ex.write(rows, 3, str('专辑编号').decode('utf-8'))
                        ex.write(rows, 4, str('在线编号').decode('utf-8'))
                        ex.write(rows, 5, str('站点名称').decode('utf-8'))
                        ex.write(rows, 6, str('开关').decode('utf-8'))
                        rows = rows + 1

                    ex.write(rows, 0, str(r[1]['zgid']).decode('utf-8'))
                    ex.write(rows, 1, str(r[1]['name']).decode('utf-8'))
                    ex.write(rows, 2, str(r[1]['grade']).decode('utf-8'))
                    ex.write(rows, 3, str(r[1]['aid']).decode('utf-8'))
                    ex.write(rows, 4, str(r[1]['box_mid']).decode('utf-8'))
                    ex.write(rows, 5, str(r[1]['site']).decode('utf-8'))
                    ex.write(rows, 6, str(r[1]['switches']).decode('utf-8'))
                    rows = rows + 1
        except IOError, e:
            logger('../jsons/', 'logger.log').write(httpResult.text)

    excel.save('../jsons/turing_grade_%s.xls' % g)
    break	
    #logger('./jsons/', ('result_%s.json' % str(g))).write(result)





