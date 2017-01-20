#!/usr/bin/env python

import sys
import logger

data = logger.logger('','users.json').load()

for item in data:
    print 'phone:%s\tuname:%s' % (item[0],item[1]) 
'''
a = sys.argv[1]

print a if a == 'OK' else 'NO'

if a == 'OK':
  print a
elif a == 'NO':
  print a
elif a == 'YES':
  print 'YES'
else:
  print 'ERROR'
'''
