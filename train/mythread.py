#!/usr/bin/env python
#-*- coding: utf-8 -*-
import threading

import time,sys
sys.path.append('..')

from common.common   import common
from common.prefixls import prefixls
from common.logger   import logger

class Mythread(threading.Thread):
    
    def __init__(self, thread_name, message, lock, thread_nums):
        self.thread_name = thread_name
        self.lock = lock
        super(Mythread, self).__init__(None, self.thread_name)
        self.message = message
	self.thread_nums = thread_nums
    
    def run(self):
        try:
            self.lock.acquire()
	    logMessage = '[%s]->%s' % (common().timeToDate(None), self.message)
	    print "线程名称:%s;\n日志:%s" % (self.thread_name, logMessage)
	    #prefixls(2, 'sheet', ('./jsons/threads_%s.xls' % self.thread_nums) ).generate( self.message )
            #logger("./jsons/","mythread.log").write(logMessage)
	    self.lock.release()
        except IOError,e:
            print e


if __name__ == '__main__':
    
    lock = threading.Lock();
    message = (('apple','orange'),('pear','banana'),('peach','watermelon'),('grape','nut'), ('Cherry','blackberry'), ('walnut','Kiwi'))
    offset = 0
    threads = []
    for item in range(0,3):
        thread_name = "apns_%s" % (item)
        #Mythread(thread_name, (message[offset:(offset+2)]), lock, item+1).start()
        threads.append(Mythread(thread_name, (message[offset:(offset+2)]), lock, item+1))
	offset = offset + 2
    	
    for k in threads:
        k.start()

    #print "threading runing %s" % threading.active_count()
    #print "Get current threading %s" % threading.current_thread()
    #for item in threading.enumerate():
    #    print item

    #定时器
    #setTimeOut()

