# -*- coding:utf-8 -*-
'''
Created on 2013-3-26

@author: zhuhua
'''
import tornado.web
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
    
    def initialize(self):
        self.errors = dict()
    
    def set_current_user(self, user):
        user = json.dumps(user)
        self.set_secure_cookie('user', user)
    
    def get_current_user(self):
        cookie = self.get_secure_cookie('user')
        try:
            return json.loads(cookie)
        except:
            return None
        
    def add_error(self, error):
        if isinstance(error, AppError):
            self.errors[error.field] = error.value
            
    def get_error(self, field='default'):
        if self.errors.has_key(field):
            return self.errors[field]
        return ''
            
    def render_json(self, data):
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.write(json.dumps(data, cls=utils.JSONEncoder))
        self.finish()
        
class Security:
    '''
    Security
    '''
    def __init__(self, *roles):
        self.roles = roles
        
    def __call__(self, method):
        
        def __method(request, *args, **kwds):
            
            user = request.get_current_user()
            if user is None:
                request.send_error(403)
                return
            
            if user['role'] not in self.roles:
                request.send_error(403)
                return
            return method(request, *args, **kwds)
        return __method
            
class AppError(Exception):
    '''Application Logic Exception'''
    def __init__(self, message, field='default'):
        self.value = message
        self.field = field
        
    def __str__(self, *args, **kwargs):
        return self.value
        
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
                
        super(Application, self).__init__(handlers, **{
            "static_path": settings.static_dir,
            "cookie_secret" : "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            "template_path": templateDir
        })