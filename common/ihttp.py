#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests,sys

class ihttp:
    
    def http_get(self, url):
        try:
           return requests.get(url)
        except Exception, e:
            print e

    def http_post(self, url, params={}, header={}):
        try:
            return requests.post(url, params, header)
        except Exception, e:
            print e
