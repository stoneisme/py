#!/usr/bin/python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self, action):
        if( hasattr(self, action) ):
            getattr(self, action)(self.get_argument('platf', 'android'), self.get_argument('mtype', 'normal'))
        else:
           self.write("Sorry, your undefined " + action + 'functions')
    
    def index(self, platf, mtype):
        self.write("Welcome to Index Controller! platf: %s; mtype: %s" % (platf, mtype))
 
    def sale(self, platf, mtype):
        self.write("Welcome to Sale Controller! platf: %s; mtype: %s" % (platf, mtype))
	
    def test(self, plaft = None, mtype = None):
        self.write('Welcome to Test Controller!')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/index/(\w*)", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


