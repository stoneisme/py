#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Create Author baihaijiang
Date 2016年10月21日
./import.py 
paltf   notify 
column  8 
sql     "select id,type,platf,state,progress,publish_at,updated_at,created_at, expires_at from messages where created_at >'2016-10-14' and created_at < '2016-10-21';" token token.xls
'''

import xlwt,sys

class prefixls:
  
    _column = 0
    _excel  = None
    _headers = {}
    _maxRows = 655535

    # 初始化
    def __init__(self, headers = {}, maxRows = 65535):
        self._headers = headers  # excel头信息
        self._column = len(self._headers)   # excel列数
        self._maxRows= maxRows  # 每个sheet表的行数
        self._excel  = xlwt.Workbook() # 创建EXCEL对象
  
    # 增加sheet表 
    def addSheet(self, sheetname):
        return self._excel.add_sheet( sheetname )

    # 保存EXCEL
    def save(self, path):
        self._excel.save(path)
   
    # 生成EXCEL文件 
    def generate(self, data, sheet = None, unsheets = 1, rows = 0):

        if len(data) < 1: #空数据返回
            sheet = self.addSheet('sheet%s' % unsheets)
            if len(self._headers) > 0:
                rows = self.write(sheet, self._headers, rows)
            return (sheet, unsheets, rows)

        for i,item in data.iteritems():
            if rows > self._maxRows:
                rows = 0
                unsheets = unsheets + 1
                sheet = None

            if rows == 0 or sheet is None:
                sheet = self.addSheet( 'sheet%s' % unsheets )
                if len(self._headers) > 0:
                    rows = self.write(sheet, self._headers, rows)
            rows = self.write(sheet, item, rows)
        return (sheet, unsheets, rows)

    # 写入EXCEL
    def write(self, sheet, item, rows):
        cols = 0
        keys = self._headers.keys()
        while cols < self._column:
            sheet.write(rows, cols, str(item[keys[cols]]).decode('utf-8'))
            cols = cols + 1
        return rows+1

if __name__ == '__main__':
    import Db
    import config.config
    import sys
    
    if len(sys.argv) < 6:
       print 'please input platf type, column num, exce SQL, sheet name, excel filename!'
       sys.exit();
       
    # notify
    # select id,type,platf,state,progress,publish_at,updated_at,created_at, expires_at from messages where created_at >'2016-10-14' and created_at < '2016-10-21';
    data = Db.Db(config.database[sys.argv[1]]).getAll( sys.argv[3])
    prefixls(int(sys.argv[2]), sys.argv[4], sys.argv[5]).generate(data)
