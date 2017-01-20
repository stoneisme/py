#!/usr/bin/python

import beanstalkc
import pickle  

try:
   c = beanstalkc.Connection(host='127.0.0.1', port=11300)
   c.use('test')
   c.put('Hello stone!')

   job = c.reserve()

   print job.body
   '''
   print job.delete()
   '''
   print 'stone'
except IOError, e:
   print e
