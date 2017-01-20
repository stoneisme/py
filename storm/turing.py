#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
sys.path.append('..')

from common.Db import Db
import config.config as config
from common.logger import logger

# remove turing
# check  save
if len(sys.argv) < 2:
    print 'argments errors'
    sys.exit()


try:
    turing = logger('../jsons/', 'save.json').load();
    string = ''
    c,n = 0,0;
    for k,v in turing.items():
        if v.has_key('vsites'):
            c = c + 1
        else:
            n = n + 1

            string += '%s,' % str(k)

            if sys.argv[1] == 'remove':
                turing.pop(k)

    print "%s:%s" % ('check', string)

    if sys.argv[1] == 'remove':
        logger('../jsons/', 'turing.json').write(turing);

    print c,n
except IOError,e:
    print e
