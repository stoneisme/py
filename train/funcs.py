#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
reload(sys)

sys.setdefaultencoding('utf-8')


def returnArgs(a,b,c):
    return a,b,c


(x,y,z) = returnArgs(1,2,3)

print x,y,z

data = range(0,10000000)
length = 1000

def filter(data, length):
    for i in xrange(0, len(data), length):
        yield data[i:i + length]


for i in filter(data,length):
    print i


