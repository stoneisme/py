#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Create Author baihaijiang
Date 2016年12月28日
Desc 统计各站点的专辑数
'''

import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding("utf-8")

from common.logger import logger
from common.prefixls import prefixls
from common.ihttp import ihttp as http
import json

class statistics:

    _turing = {}  # 影片信息
    _grade = {}   # 渠道信息
    _extra = {}   # 地域等级
    _type = {}    # 影片类型
    _sites = []   # 站点信息
    _params = {}  # 接口参数
    _api = 'http://i.turing.shouji.baofeng.com/cgi/album/details'  # 图灵接口地址
    _albumIds = []  # 影片编号
    _albumslen = 0  # 影片数量
    _result    = {}


    def __init__(self, params, grades, turing, albumTypes, extra, sites):
        self._extra      = extra
        self._turing     = turing
        self._type       = albumTypes
        self._params     = params
        self._grade      = grades
        self._sites      = sites
        self._albumIds   = self._turing.keys()
        self._albumslen  = len(self._albumIds)

    '''
          线程运行
        '''

    def run(self):
        try:
            # self.lock.acquire()
            self.getAlbums()
            # self.lock.release()
        except IOError, e:
            print e

    '''
      获取专辑信息
    '''

    def getAlbums(self):

        offset = 0
        limit = 2000

        while (offset < self._albumslen):

            s = offset
            e = offset + limit
            offset = e

            aids = []

            if (e > self._albumslen):
                aids = self._albumIds[s:]
            else:
                aids = self._albumIds[s:e]

            self._params['albums'] = {}
            self._params['aids'] = ",".join(str(kk) for kk in aids)

            albums = {}
            extras = {}

            for t in aids:
                albums[t] = {}
                albums[t] = self._turing[t]
                if self._extra[t] is not None:
                    extras[t] = {}
                    extras[t] = self._extra[t]

            self._params['albums'] = json.dumps(albums)
            self._params['extra'] = json.dumps(extras)

            self.turing()

        logger('../jsons/', 'statistics_%s.json' % self._params['grade']).write(self._result)

    '''
      调用图灵接口获取可播站点以及顺序
    '''
    def turing(self):
        try:
            httpResult = http().http_post(self._api, self._params)
            ret = httpResult.json()
            if ret['status'] == 1:
                for r in ret['result'].iteritems():
                    if len(r[1]['turing_mode']) > 0:
                        for m in r[1]['turing_mode'].iteritems():
                            if not self._result.has_key(self._params['grade']):
                                self._result[self._params['grade']] = {}

                            if not self._result[self._params['grade']].has_key(self._turing[r[1]['id']]['type']):
                                self._result[self._params['grade']][self._turing[r[1]['id']]['type']] = {}

                            if not self._result[self._params['grade']][self._turing[r[1]['id']]['type']].has_key(str(m[1]['site'])):
                                self._result[self._params['grade']][self._turing[r[1]['id']]['type']][str(m[1]['site'])] = 0

                            if str(m[1]['site']).decode('utf-8') in self._sites:
                                self._result[self._params['grade']][self._turing[r[1]['id']]['type']][
                                    str(m[1]['site'])] = self._result[self._params['grade']][self._turing[r[1]['id']]['type']][str(m[1]['site'])] + 1
        except IOError, e:
            logger('../jsons/', 'logger.log').write(httpResult.text)



class reports:
    _exRows = 1  # excel行数
    _exSheet = 1  # excel的sheet表
    _exSheetObj = None
    _data = {}
    _grades = {}
    _type = {}
    _grade = {}
    _headers = {'grade': '渠道', 'site': '站点名称', 'type': '专辑类型', 'count': '专辑数量'}

    def __init__(self, grade):
        self._data   = logger('../jsons/', 'statistics_%s.json' % grade).load()
        self._grades = logger('../jsons/', 'grade.json').load()
        self._type   = logger('../jsons/', 'albumTypes.json').load()
        self._grade  = grade

    def generate(self):
        prefixlsObj = prefixls(self._headers)
        result = {}
        index = 0;
        for key,value in self._data.items():
            for kk,vv in value.items():
                for ks,vs in vv.items():
                    result[index] = {}
                    result[index]['grade'] = self._grades[int(key)]['name']
                    result[index]['site']  = ks
                    result[index]['type']  = self._type[kk]['name']
                    result[index]['count'] = vs
                    index = index + 1
        prefixlsObj.generate(result, self._exSheetObj, self._exSheet, self._exRows)
        prefixlsObj.save('../jsons/reports_%s.xls' % self._grade)

if __name__ == '__main__':


    if sys.argv[1] == 'statistics':
        turing     = logger('../jsons/', 'turing.json').load()
        extra      = logger('../jsons/', 'extra.json').load()
        sites      = logger('../jsons/','sites.json').load()
        grades     = logger('../jsons/', 'grade.json').load()
        albumTypes = logger('../jsons/', 'albumTypes.json').load()
        params = {'platf': 'android', 'ver': '7.0.03', 'mtype': 'normal', 'grade': sys.argv[2]}
        statistics(params, grades, turing, albumTypes, extra, sites).run()
    elif sys.argv[1] == 'reports':
        reports(sys.argv[2]).generate()
