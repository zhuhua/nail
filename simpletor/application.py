# -*- coding:utf-8 -*-
'''
Created on 2013-3-26

@author: zhuhua
'''
import tornado.web
import tornado.template
import json
import utils
import settings

class RequestMapping:
    
    def __init__(self, value):
        self.value = value
    
    def __call__(self, handler):
        self.handler = handler
        return self
    
class RequestHandler(tornado.web.RequestHandler):
    
    def render_json(self, data):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(data, cls=utils.JSONEncoder))
        self.finish()
        
class AppError(Exception):
    '''Application Logic Exception'''
    pass
    
class Application(tornado.web.Application):
    
    def __init__(self):
        
        handlers = []
        installedApps = settings.installed_apps
        
        for appName in installedApps:
            appPackage = __import__(appName, globals(), locals(), ['views'], -1)
            views = appPackage.views

            for handlerName in dir(views):
                handlerWrapper = getattr(views, handlerName)
                if isinstance(handlerWrapper, RequestMapping):
                    handlers.append((handlerWrapper.value, handlerWrapper.handler))
                    
        templateDir = settings.template_dir
        self.template = tornado.template.Loader(templateDir)
                
        super(Application, self).__init__(handlers, **{
            "static_path": settings.static_dir
        })