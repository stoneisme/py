#!/usr/bin/env python
#-*- coding: utf-8 -*- 

import MySQLdb
import MySQLdb.cursors

class Db:
    def __init__(self, database):
        self.__host   = database['host']
        self.__port   = database['port']
        self.__dbname = database['dbname']
        self.__user   = database['user']
        self.__pass   = database['pass']
        self.__charset= database['charset']
        self.__db     = False
        self.__cursor = False
        self.connect()

    def connect(self):
        try:
            self.__db = MySQLdb.Connect(
                        host=self.__host,
                        port=self.__port,
                        user=self.__user,
                        passwd=self.__pass,
                        db=self.__dbname,
                        charset=self.__charset,
                        autocommit=True,
                        cursorclass = MySQLdb.cursors.DictCursor
                    )
            self.__cursor = self.__db.cursor()
        except Exception, e:
            print e
   
    def getAll(self, sql):
        try:
            self.__cursor.execute(sql)
            return  self.__cursor.fetchall()
        except Exception, e:
            return []
  
    def getRow(self, sql):
        try:
            self.__cursor.execute( sql )
            return self.__cursor.fetchone()
        except Exception, e:
            return []

    def update(self, sql):
        try:
            self.__cursor.execute(sql)
            return
        except Exception, e:
            return 0

    def insert(self,sql):
        try:
            self.__cursor.execute(sql)
            return self.__db.insert_id()
        except Exception, e:
            return 0
			
    def close(self):
        if self.__db:
            self.__cursor.close()
            self.__db.close()

    def __del__(self):
        self.close()


if __name__ == '__main__':
   import config as config
   import logger
   rows = Db(config.database['local']).getAll("SELECT user_name,phone FROM 91pigou_users ORDER BY user_id ASC")
   logger.logger('','users.json').write(rows)

