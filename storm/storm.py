#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Create Author baihaijiang
Date 2016年11月21日
Desc 导出影片信息
'''

import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding("utf-8")

from common.logger import logger
from common.prefixls import prefixls
from common.ihttp import ihttp as http
import json
import threading

class storm(threading.Thread):
    	
    _turing     = {} #影片信息
    _grade      = {} #渠道信息
    _extra      = {} #地域等级
    _type       = {} #影片类型
    _headers    = {'switchs':'开关','site':'站点名称','box_mid':'在线编号','title':'专辑名称','type':'专辑类型','aid':'专辑编号','grade':'渠道编号','name':'渠道名称','zgid':'地域编号'}
    _params     = {} #接口参数
    _api        = 'http://i.turing.shouji.baofeng.com/cgi/album/details' #图灵接口地址
    _albumIds   = [] #影片编号
    _albumslen  = 0  #影片数量
    _exRows     = 1  #excel行数
    _exSheet    = 1  #excel的sheet表
    _exSheetObj = None

    '''
      初始化数据	
    '''	
    def __init__(self, params, grades, turing, albumTypes, extra, thread_name):
        self._extra      = extra
        self._turing     = turing
        self._type       = albumTypes
        self._params     = params
        self._grade      = grades
        self._albumIds   = self._turing.keys()
        self._albumslen  = len(self._albumIds)
        self.thread_name = thread_name
        #self.lock = lock
        super(storm, self).__init__(None, self.thread_name)

    '''
      线程运行
    '''
    def run(self):
        try:
            #self.lock.acquire()
            self.getAlbums()
            #self.lock.release()
        except IOError,e:
            print e

    '''
      获取专辑信息
    '''
    def getAlbums(self):

        prefixlsObj = prefixls(self._headers)

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
            self._params['extra']  = json.dumps(extras)
            (self._exSheetObj, self._exSheet, self._exRows) = prefixlsObj.generate(self.turing(), self._exSheetObj, self._exSheet, self._exRows)
        prefixlsObj.save( '../jsons/%s_%s_%s.xls' % (self._params['platf'], self._params['mtype'], self._params['grade']))
    
    '''
      调用图灵接口获取可播站点以及顺序
    '''
    def turing(self):
        try:
            httpResult = http().http_post(self._api, self._params)
            ret = httpResult.json()
            if ret['status'] == 1:
                return self.hanleTuring( ret['result'] )
        except IOError, e:
            logger('../jsons/', 'logger.log').write(httpResult.text)

   
    '''
      处理图灵接口返回数据
    '''
    def hanleTuring(self, data):
        index = 0
        result = {}
        for ret in data.iteritems():
            result[index] = {}
            if len(ret[1]['turing_mode']) > 0:
                for m in ret[1]['turing_mode'].iteritems():
                    result[index] = {}
                    result[index]['zgid']    = str(self._grade[self._params['grade']]['zgid'])
                    result[index]['name']    = str(self._grade[self._params['grade']]['name'])
                    result[index]['grade']   = str(self._params['grade'])
                    result[index]['aid']     = str(ret[1]['id'])
                    result[index]['type']    = str(self._type[self._turing[ret[1]['id']]['type']]['name'])
                    result[index]['title']   = str(self._turing[ret[1]['id']]['title'])
                    result[index]['box_mid'] = str(self._turing[ret[1]['id']]['box_mid'])
                    result[index]['site']    = str(m[1]['site']).decode('utf-8')
                    result[index]['switchs'] = str(m[1]['switches']).decode('utf-8')
                    index = index + 1
            else:
                result[index]['zgid']        = str(self._grade[self._params['grade']]['zgid'])
                result[index]['name']        = str(self._grade[self._params['grade']]['name'])
                result[index]['grade']       = str(self._params['grade'])
                result[index]['aid']         = str(ret[1]['id'])
                result[index]['type']        = str(self._type[self._turing[ret[1]['id']]['type']]['name'])
                result[index]['title']       = str(self._turing[ret[1]['id']]['title'])
                result[index]['box_mid']     = str(self._turing[ret[1]['id']]['box_mid'])
                result[index]['site']        = ''
                result[index]['switchs']     = 0
                index = index + 1
        return result



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'arguments errors!'
        sys.exit()

    platf = sys.argv[1]
    mtype = sys.argv[2] 
    
    platfs = ['android','iphone','ipad']
    mtypes = ['high','normal','middle','lowend']
    
    pg     = int(sys.argv[3])

    if platf not in platfs:
        print 'platf is error'
        sys.exit()
    
    if mtype not in mtypes:
        print 'mtype is error'
        sys.exit()
	
    turing = logger('../jsons/', 'turing.json').load()

    extra  = logger('../jsons/', 'extra.json').load()

    grades  = logger('../jsons/', 'grade.json').load()
    
    albumTypes = logger('../jsons/', 'albumTypes.json').load()

    #lock = threading.Lock()
    
    limit  = 3;
    offset = (pg - 1) * limit;

    gr = grades.keys()
    
    g  = gr[offset:offset+limit]

    for grade in g:
        params = {'platf':platf,'ver':'7.0.03', 'mtype':mtype,'grade':grade}
        thread_name = "%s_%s_%s" % (platf, mtype, grade)
        storm(params, grades, turing, albumTypes, extra, thread_name).start()
