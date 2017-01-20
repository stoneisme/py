#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
sys.path.append('..')

from common.Db import Db
import config.config as config
from common.logger import logger

class albums:

     _data = {}
     
     '''
	 获取专辑ID
     '''
     def getAlbumIds(self):
         #sql = 'SELECT a.id AS id,a.type AS type, a.title AS title, a.box_mid,a.status FROM albums AS a WHERE a.box_mid > 0 AND a.status > 0'
         sql = 'SELECT a.id AS id,a.type AS type, a.title AS title, a.box_mid, a.status FROM albums AS a WHERE a.status IN (1,3,5,7) AND type IN (1,2,3,4)'
         return Db(config.database['storm']).getAll( sql )

     def saveAlbumIds(self, opt):
         albumIds = self.getAlbumIds();
         for album in albumIds:
             self._data[album['id']] = {}
             self._data[album['id']] = album
         logger('../jsons/', opt + '.json').write(self._data)
     
     '''
	 获取专辑类型
     '''		
     def getAlbumTypes(self):
         sql = "SELECT id,name FROM album_type ORDER BY id ASC "
         return  Db(config.database['storm']).getAll( sql )

     def saveAlbumTypes(self, opt):
         albumTypes = self.getAlbumTypes()
         types = {}
         for t in albumTypes:
             types[t['id']] = t
         logger('../jsons/', opt + '.json').write(types)

     '''
     获取专辑站点
     '''
     def getAlbumSites(self, platf = 'android'):
         sql = "SELECT id,site FROM sites_status WHERE platf = '%s' ORDER BY id ASC" % platf
         return Db(config.database['storm']).getAll(sql)

     def saveAlbumSites(self, opt):
         albumSites = self.getAlbumSites()
         sitesInfo = []
         for sites in albumSites:
             sitesInfo.append(sites['site'])
         logger('../jsons/', opt + '.json').write(sitesInfo)

     '''
      获取专辑分级
     '''
     def getAlbumExtra(self, albumIdStr):
         sql = 'SELECT album_id AS aid, agid, grades, album_offline FROM album_extra WHERE album_id IN (%s)'
         return Db(config.database['storm']).getAll( (sql % albumIdStr) )
     
     
     def handleAlbumExtra(self, extras):
         for item in extras:
             self._data[item['aid']] = {}
             self._data[item['aid']] = item


     '''
      保存专辑分级
     '''
     def saveAlbumExtra(self, opt):
         albumIds = (logger('../jsons/', 'albums.json').load()).keys()
        
         albumIdStr = ''

         record = len(albumIds)

         offset = 0
         limit = 10000
         k = 0

         while( offset < record):
             s = offset
             e = offset + limit
             offset = offset + limit
             k = k + 1

             if ( e > record ):
                albumIdStr = ",".join(str(kk) for kk in albumIds[s:])
             else:
                albumIdStr = ",".join(str(kk) for kk in albumIds[s:e])
             self.handleAlbumExtra(self.getAlbumExtra(albumIdStr))

         logger('../jsons/', opt + '.json').write(self._data)


     '''
      获取地域等级
     '''
     def getGroupsZone(self):
         sql = 'SELECT id AS zgid,name,grade FROM groups_zone WHERE grade > 0'
         return Db(config.database['storm']).getAll( sql )


     def saveGroupsZone(self, opt):
         groupsZone = self.getGroupsZone();
         for zone in groupsZone:
             self._data[zone['grade']] = zone
         logger('../jsons/', opt + '.json').write(self._data)

     def main(self, opt):
        if opt == 'albums':
            self.saveAlbumIds( opt )
        elif opt == 'extra':
            self.saveAlbumExtra( opt )
        elif opt == 'grade':
            self.saveGroupsZone( opt )
        elif opt == 'albumTypes':
            self.saveAlbumTypes( opt )
        elif opt == 'sites':
            self.saveAlbumSites( opt )
        else:
            print 'arguments errors'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'arguments errors'
        sys.exit()
    
    albums().main(sys.argv[1])
