#!/usr/bin/env python
#-*- coding: utf-8 -*-
import threading
from common.Db import Db
import config.config as config
import time,sys

class Mythread(threading.Thread):
    
    def __init__(self, thread_name, message, lock):
        self.thread_name = thread_name
        self.lock = lock
        super(Mythread, self).__init__(None, self.thread_name)
        self.message = message
        self.runing = True
        #threading.Thread.__init__(self, None, thread_name)

    def stop(self):
        self.runing = False

    def run(self):
        while self.runing:
            try:
                self.lock.acquire()
                print self.thread_name
                print self.message
            except IOError,e:
                print e


def setTimeOut():
    print "Hello World %s " % time.strftime("%Y-%m-%d %H:%M:%S")
    threading.Timer(120, setTimeOut).start()


if __name__ == '__main__':
    lock = threading.Lock();
    threads = []
    threadnum = 1
    message = Db(config.database['local']).getAll('SELECT user_name,phone FROM 91pigou_users')
    print 'len %d' % len(message)
    for item in message:
        thread_name = "%s_apns_%s_%d" % ('iphone', item[1], threadnum)
        threads.append(Mythread(thread_name, item, lock))
	threadnum = threadnum + 1

    for k in threads:
        k.start()

    print "threading runing %s" % threading.active_count()
    print "Get current threading %s" % threading.current_thread()
    for item in threading.enumerate():
        print item

    #定时器
    #setTimeOut()

