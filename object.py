#!/usr/bin/env python

class a(object):
    def __init__(self):
        super(a, self)
        print "__init__"

    def test(self, say):
        print "Hi, " + say


a().test('stone')