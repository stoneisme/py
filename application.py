#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys

if len(sys.argv) < 2:
    print 'arguments errors!'
    sys.exit()	

if sys.argv[1] == 'storm':
    from storm.albums import albums

albums().main('grade')

