#!/usr/bin/env python
# -*- coding: utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo

class mongodb:
    _host    = None
    _port    = None
    _dbname  = None
    _user    = None
    _pass    = None
    _timeout = 3000
    _mongodb = None

    def __init__(self, database):
        self._host    = database['host']
        self._port    = database['port']
        self._user    = database['user']
        self._pass    = database['pass']
        self._dbname  = database['dbname']
        self._timeout = database['timeout'] if database['timeout'] else self._timeout
        self._mongodb = pymongo.MongoClient('mongodb://%s:%s@%s:%s/%s?connectTimeoutMS=%s' % (self._user,self._pass,self._host,self._port, self._dbname, self._timeout))

    # 获取集合对象
    def get_stmt(self, table):
        return self._mongodb[self._dbname][table]

    def count(self, table, condition = {}):
        try:
            return self.get_stmt(table).find(condition).count()
        except:
            return 0

    # 获取多个集合
    def getAll(self, table, condition = {}, offset = 0, limit = 10, fields = {}):
        try:
            return self.get_stmt(table).find(condition, fields).skip(offset).limit(limit)
        except:
            return {}

    # 获取一个集合
    def getRow(self, table, condition, fields={}):
        try:
            return self.get_stmt(table).find_one(condition, fields)
        except:
            return {}

    def getOne(self, table, condition, fields={}, field = None):
        try:
            if field is None:
                return self.getRow(table,condition, fields)
            return self.getRow(table,condition, fields).pop(field)
        except:
            return ''

    # 更新集合
    def update(self, table, condition, data):
        if not condition:
            return False
        return self.get_stmt(table).update(condition, data)

    # 插入集合
    def insert(self, table, data):
        if not data:
            return False
        return self.get_stmt(table).insert(data)

    # 批量插入集合
    def insert_batch(self, table, data):
        if not data:
            return
        return self.get_stmt(table).insert_many(data)

    # 删除集合
    def delete(self, table, condition):
        if not condition:
            return
        return self.get_stmt(table).remove(condition)

    def __del__(self):
        self._mongodb.close()

