# -*- coding:utf-8 -*-
'''
Created on 2014年12月18日

@author: zhuhua
'''
from simpletor import application

from user import services as user_service
from artisan import services as artisan_service
from sample import services as sample_service

def api(method):
    def __method(handler, *args, **kwds):
        headers = handler.request.headers
        if not headers.has_key('Token'):
            handler.send_error(403)
            return
        
        token = user_service.get_token(headers['token'])
        if token is None:
            handler.send_error(403)
            return
        handler.set_current_user(dict(id=token.user_id))
        return method(handler, *args, **kwds)
    return __method

#######  USER ##################################
@application.RequestMapping("/api/user/register")
class Register(application.RequestHandler):
    def post(self):
        mobile = self.get_argument('mobile', strip=True)
        password = self.get_argument('password', strip=True)
        checkcode = self.get_argument('checkcode', strip=True)
        user_service.register(mobile, password)

@application.RequestMapping("/api/user/login")
class Login(application.RequestHandler):
    def post(self):
        mobile = self.get_argument('mobile', strip=True)
        password = self.get_argument('password', strip=True)
        token = user_service.login(mobile, password)
        self.render_json(token)
       
@application.RequestMapping("/api/user/profile") 
class UserProfile(application.RequestHandler):
    @api
    def post(self):
        user_id = self.get_current_user()['id']
        user = user_service.get_profile(user_id)
        self.render_json(user)

#######  ARTISAN ##################################
@application.RequestMapping("/api/artisans")
class Artisans(application.RequestHandler):
    def post(self):
        order_by = self.get_argument('order_by', default='', strip=True)
        sort = self.get_argument('sort', default='asc', strip=True)
        page = self.get_argument('page', default=1, strip=True)
        dis_size = self.get_argument('dis_size', default=10, strip=True)
        name = self.get_argument('name', default = '', strip=True)
        artisans = artisan_service.search_artisan(page, dis_size, name, order_by, sort)
        self.render_json(artisans)
        
@application.RequestMapping("/api/artisan")
class Artisan(application.RequestHandler):
    def post(self):
        artisan_id = self.get_argument('id', strip=True)
        artisan = artisan_service.get_artisan(artisan_id)
        self.render_json(artisan)
        
#######  SAMPLE ##################################
@application.RequestMapping("/api/samples")
class Samples(application.RequestHandler):
    def post(self):
        order_by = self.get_argument('order_by', default='', strip=True)
        sort = self.get_argument('sort', default='asc', strip=True)
        page = self.get_argument('page', default=1, strip=True)
        dis_size = self.get_argument('dis_size', default=10, strip=True)
        artisan_id = self.get_argument('artisan_id', default='', strip=True)
        
        samples, hits = sample_service.search_sample(page, dis_size, artisan_id)
        self.render_json(samples)
     
@application.RequestMapping("/api/sample")
class Sample(application.RequestHandler):
    def post(self):
        sample_id = self.get_argument('id', strip=True)
        sample = sample_service.get_sample(sample_id)
        self.render_json(sample)