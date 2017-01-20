#!/usr/bin/env python
#-*- coding: utf-8 -*-  

'''
Create Author baihaijiang
Date 2016-10-24
Desc 发送邮件
'''

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class mail:
  
   __host    = None #邮件服务器
   __user    = None #邮件帐号
   __pass    = None #邮件密码
   __charset = None #邮件编码
   __toAddr  = []   #收件人
   
   #初始化邮件服务器
   def __init__(self, bf):
      self.__host    = bf['host']
      self.__user    = bf['user']
      self.__pass    = bf['pass']
      self.__charset = bf['charset']
      self.__toAddr  = bf['to']
      
      try:
         self._server = smtplib.SMTP()
         self._server.connect(self.__host)
         self._server.login(self.__user, self.__pass)
         self._msg = MIMEMultipart()
      except Exception, e:
         print e

   #增加邮件附件
   def add_attach(self, filename):
      attach = MIMEText(open(filename, 'rb').read(), 'base64', self.__charset)
      attach["Content-Type"] = 'application/octet-stream'
      attach["Content-Disposition"] = 'attachment; filename="'+filename+'"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
      self._msg.attach(attach)

   #发送邮件
   def send_msg(self, to_addr = [], subject = '', content = '', filename = ''):
      try:

        self._msg['From'] = self.__user
       
        if len(to_addr) > 0:
           self._msg['To']   = ",".join(to_addr)
        else:
           self._msg['To']   = ",".join(self.__toAddr)
           
        self._msg['Subject'] = subject

        #增加内容
        body = MIMEText(content, _subtype='html', _charset=self.__charset)
        self._msg.attach(body)

        #增加附件
        if len(filename) > 0:
           self.add_attach(filename)

        self._server.sendmail(self._msg['From'], self.__toAddr, self._msg.as_string())
        self._server.close()
        return True
      except Exception, e:
        print e
        return False



if __name__ == '__main__':
   import config.config
   content = "<div>"
   content+= "<div>Hi all</div>"
   content+= "<div style='margin-left:15px;'>附件是token数据，请查收，如有问题联系我！</div>"
   content+= "</div>"

   if mail(config.mail['baofeng']).send_msg([], 'token数据', content, 'token.xls'):
      print "发送成功"
   else:
      print "发送失败"
