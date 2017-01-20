#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys,json,os
sys.path.append('..')

import config.config as config
from common.prefixls import prefixls
from common.Db import Db
from common.mongodb import mongodb
from common.mail import mail


def send_mail(opt, title, filepath):
   content = "<div>"
   content+= "<div>Hi all</div>"
   content+= "<div style='margin-left:15px;'>附件是"+title+"数据，请查收，如有问题联系我！</div>"
   content+= "</div>"
   config.mail['baofeng']['to'] = ['wuliqiang@baofeng.com']
   if mail(config.mail['baofeng']).send_msg([], title+'数据', content, filepath):
      if os.path.exists( filepath ):
         os.remove( filepath )
      print "MAIL STATUS: 发送成功"
   else:
      print "MAIL STATUS: 发送失败"

if __name__ == '__main__':
    if sys.argv[1] == 'messages':
        sql = 'SELECT alert,custom,platf,publish_at,expires_at,created_at FROM messages WHERE type IN(1) AND checked = 1 AND (created_at > "%s" AND created_at < "%s") '

        messages = Db(config.database['notify']).getAll( sql % (sys.argv[2],sys.argv[3]) )

        ret = {}
        if len(messages):
            index = 0
            for item in messages:
                ret[index] = {}
                ret[index]['alert']      = item['alert']
                ret[index]['custom']     = json.loads(item['custom'])['albumid']
                ret[index]['platf']      = item['platf']
                ret[index]['publish_at'] = item['publish_at']
                ret[index]['expires_at'] = item['expires_at']
                ret[index]['created_at'] = item['created_at']
                index = index + 1

        filepath = '../jsons/messages.xls'
        headers = {"alert": "推送内容", "custom": "专辑ID","platf":"平台","publish_at":"开始时间","expires_at":'结束时间','created_at':"创建时间"}

        prefixlsObj = prefixls(headers)  # 建EXCEL
        prefixlsObj.generate(ret)  # 写EXCEL
        prefixlsObj.save(filepath)  # 保EXCEL

        send_mail('messages', 'IOS推送消息', filepath)  # 发送邮件

    elif sys.argv[1] == 'notify':
        limit = 5

        offset = 10  # ( int(sys.argv[1]) - 1 ) * limit

        table, condition, fields = 'tokens_iphone', {'common_switch': 1}, {"_id": 0, 'token': "", 'device_id': "",
                                                                          "version": "", "started_time": "", "area": ""}

        condition["version"] = {'$gte': 320000}
        condition['started_time'] = {"$exists": 'true'}
        # condition['area'] = [{"$exists":"true"}, {"$eq":23}]

        mongodbClient = mongodb(config.mongodb['ios_notify'])
        # print mongodbClient.count( table, condition )


        data = mongodbClient.getAll(table, condition, offset, limit, fields)

        for d in data:
            # print 'token: %s, version: %s, device_id: %s, started_time: %s, area: %s' % (d['token'], d['version'], d['device_id'], d['started_time'], d['area'])
            print 'token: %s, version: %s, device_id: %s' % (d['token'], d['version'], d['device_id'])

        print mongodbClient.getRow(table, condition, fields)
        print mongodbClient.getOne(table, condition, fields, 'token')
    else:
        print 'argument errors'

