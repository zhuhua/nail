'''
Created on 2013-3-26

@author: zhuhua
'''
import tornado.httpserver
import tornado.ioloop

import application
import settings
         
if __name__ == '__main__':

    server = tornado.httpserver.HTTPServer(application.Application())
    server.listen(settings.port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()