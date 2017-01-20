#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
sys.path.append('..')

from common.Db import Db
import config.config as config
from common.logger import logger

class videos:

    _data = {}
    _allstatus = [1,3,5,7]

    def __init__(self):
        self._albums = logger('../jsons/', 'albums.json').load();

    def getSitesInfo(self, albumIdStr):
        sql = 'SELECT v.album_id,  GROUP_CONCAT(DISTINCT v.site) AS vsites, v.status AS status FROM videos AS v '
        '''
        sql+= ' WHERE v.album_id IN (%s) AND v.site IN (%s) GROUP BY v.album_id ';
    
        sites = ['bf-1080', 'bf-240', 'bf-480', 'bf-720','bf-h5','bf-HD1080','bf-HD720','bf-short','bf-抢先'];
        sql = sql % (albumIdStr, ','.join("'"+s+"'" for s in sites) )
        '''

        sql += ' WHERE v.album_id IN (%s) AND v.status IN (1, 3, 5, 7) GROUP BY v.album_id ';
        #sql += ' WHERE v.album_id IN (%s) GROUP BY v.album_id ';

        #sites = ['bf-1080', 'bf-240', 'bf-480', 'bf-720', 'bf-h5', 'bf-HD1080', 'bf-HD720', 'bf-short', 'bf-抢先'];
        sql = sql % (albumIdStr)
        
        return Db(config.database['storm']).getAll( sql )

    
    def getAlbums(self):
        albumIds = self._albums.keys()
        
        albumIdStr = ''

        record = len(albumIds)

        offset = 0
        limit = 10000
   	
        while( offset < record):
            s = offset
            e = offset + limit
            offset = offset + limit

            if ( e > record ):
               albumIdStr = ",".join(str(kk) for kk in albumIds[s:])
            else:
               albumIdStr = ",".join(str(kk) for kk in albumIds[s:e])
            self.handelVideos(self.getSitesInfo(albumIdStr))

	
    def handelVideos(self, videos ):
        for item in videos:
            self._albums[item['album_id']]["vsites"] = item['vsites']

    def saveAlbums(self):
        self.getAlbums()
        logger('../jsons/','save.json').write(self._albums)

    def main(self, opt):
        if opt == 'videos':
            videos().saveAlbums()
        else:
            print 'arguments errors'
	


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'arguments errors'
        sys.exit()

    videos().main(sys.argv[1])
