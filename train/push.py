#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define, options
from apnsclient.apns import APNs, Message
from apnsclient.transport import Session

class PushApplication():
    def __init__(self):
        '''
        PushApplication init
        '''
        app_handlers = []

        app_settings = dict(
            # debug=True,
        )

        session = Session()

        self.conn = self.session.get_connection("push_production",
                                                **self.params)
        self.service = APNs(self.conn)

        tornado.web.Application.__init__(self, app_handlers, **app_settings)

def main():
    http_server = tornado.httpserver.HTTPServer(PushApplication())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
