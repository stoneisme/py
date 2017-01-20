#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Create Author baihaijiang
Date 2016年11月21日
Desc 发送Token信息
'''

import sys
sys.path.append('..')

from common.mail import mail
from common.prefixls import prefixls
from common.Db import Db
from common.common import common
import config.config as config
import pytz
import os

pytz.timezone('Asia/Shanghai')

def send_mail(opt, title, filepath):
   content = "<div>"
   content+= "<div>Hi all</div>"
   content+= "<div style='margin-left:15px;'>附件是"+title+"数据，请查收，如有问题联系我！</div>"
   content+= "</div>"
   if mail(config.mail['baofeng']).send_msg([], title+'数据', content, filepath):
      if os.path.exists( filepath ):
         os.remove( filepath )
      print "MAIL STATUS: 发送成功"
   else:
      print "MAIL STATUS: 发送失败"


def getData(database):
   
   edate = common().timeToDate(None, "%Y-%m-%d")
   sdate = common().daysToDate(edate, d = -7, fmt = "%Y-%m-%d")
      
   #sql = "SELECT id,type,platf,state,progress,publish_at,updated_at,created_at, expires_at FROM messages "
   sql = "SELECT platf,progress,publish_at,expires_at,updated_at,created_at FROM messages "
   sql+= "WHERE created_at >'%s' and created_at < '%s'"
      
   print "[%s]执行SQL：%s"  % (common().timeToDate(None), sql % (sdate, edate))
   
   data =  Db(database).getAll( sql % (sdate, edate) )

   ret = {}
   if len(data):
       index = 0
       for item in data:
           ret[index] = {}
           ret[index] = item
           index = index + 1

   return ret

def main(opt):
    if opt == 'token':
        data = getData(config.database['notify']);
        filepath = '../jsons/%s.xls' % opt
        headers = {"platf":"平台","progress":"已推送数量/总推数量","publish_at":"推送开始时间","expires_at":"推送失效时间","updated_at":"进度/状态更新时间","created_at":"创建时间"}

        prefixlsObj = prefixls(headers) # 建EXCEL
        prefixlsObj.generate( data )    # 写EXCEL
        prefixlsObj.save(filepath)      # 保EXCEL

        send_mail(opt, opt, filepath) #发送邮件
	
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'argument params errors'
        sys.exit()
    main(sys.argv[1])
