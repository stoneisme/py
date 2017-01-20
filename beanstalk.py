#!/usr/bin/python   
#-*- coding: utf-8 -*-  
''' 
Created on 2016年9月13日 
@author: baihaijiang
'''  
  
import beanstalkc  
import config.config as config
  
  
class BSQueueC():  
      
    def __init__(self, host, port=11300):  
        self.host = host  
        self.port = port  
        self.__conn = beanstalkc.Connection(host, port)  
          
    def __del__(self):  
        self.__conn.close()  
          
    def put(self,tube, body, priority=2**31, delay=0, ttr=120):  
        self.__conn.use(tube)  
        return self.__conn.put(body, priority, delay, ttr)  
      
    def reserve(self, tube, timeout=20):  
        for t in self.__conn.watching():  
            self.__conn.ignore(t)  
        self.__conn.watch(tube)  
        return self.__conn.reserve(timeout)  
      
    def clear(self, tube):  
        try:  
            while 1:  
                job = self.reserve(tube, 1)  
                if job is None:  
                    break  
                else:  
                    job.delete()  
        except Exception, e:  
            print 


if __name__ == '__main__':
    obj = BSQueueC(config.beanstalkd['host'], config.beanstalkd['port'])
    obj.put('test','Hello World!')
    data = obj.reserve('test');
    print data.body
    
