# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/6/5 14:54"

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('hello world')

    def post(self, *args, **kwargs):
        pass


class TestHandler(tornado.web.RequestHandler):
    def get(self, name):
        self.write('hi, welcome %s' % name)


if __name__ == '__main__':
    url_router = [
        (r'/', MainHandler),
        (r'/test/(.*)', TestHandler)
    ]

    application = tornado.web.Application(url_router)
    application.listen(8887)
    tornado.ioloop.IOLoop.instance().start()



