#!/usr/bin/env python
#-*- coding: utf-8 -*- 

import os
import sys

class logger:
  
    def __init__(self, path, filename):
        self.__filepath = path + filename


    def write(self, data):
        try:
            handle = open(self.__filepath, "a+")
            print >> handle, data
            handle.close()
        except IOError, e:
            print e

    def load(self):
        """方法说明
        加载容易改变的配置
        """
        try: 
            with open(self.__filepath) as config:
                configs = eval(config.read())
            return configs
        except IOError,e:
            print e
