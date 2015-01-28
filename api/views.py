# -*- coding:utf-8 -*-
'''
Created on 2014年12月18日

@author: zhuhua
'''
from simpletor import application

from user import services as user_service
from artisan import services as artisan_service
from sample import services as sample_service
from common import services as common_service

class Api():
    def __init__(self, auth=False):
        self.auth = auth
    
    def __call__(self, method):
        def __method(handler, *args, **kwds):
            headers = handler.request.headers
            if self.auth:
                if not headers.has_key('Token'):
                    handler.send_error(403)
                    return
                
                token = user_service.get_token(headers['token'])
                if token is None:
                    handler.send_error(403)
                    return
                handler.set_current_user(dict(id=token.user_id))
            try:
                method(handler, *args, **kwds)
            except application.AppError, e:
                handler.render_json(dict(message=e.value))
        return __method

#######  USER ##################################
@application.RequestMapping("/api/user/register")
class Register(application.RequestHandler):
    @Api()
    def post(self):
        mobile = self.get_argument('mobile', strip=True)
        password = self.get_argument('password', strip=True)
        checkcode = self.get_argument('checkcode', strip=True)
        
        if not checkcode == '111111':
            raise application.AppError('验证码错误')
        
        user_service.register(mobile, password)

@application.RequestMapping("/api/user/login")
class Login(application.RequestHandler):
    @Api()
    def post(self):
        mobile = self.get_argument('mobile', strip=True)
        password = self.get_argument('password', strip=True)
        token = user_service.login(mobile, password)
        self.render_json(token)
       
@application.RequestMapping("/api/user/profile") 
class UserProfile(application.RequestHandler):
    @Api(auth=True)
    def get(self):
        user_id = self.get_current_user()['id']
        user = user_service.get_profile(user_id)
        self.render_json(user)

#######  ARTISAN ##################################
@application.RequestMapping("/api/artisans")
class Artisans(application.RequestHandler):
    @Api()
    def get(self):
        order_by = self.get_argument('order_by', default='', strip=True)
        sort = self.get_argument('sort', default='asc', strip=True)
        page = self.get_argument('page', default=1, strip=True)
        dis_size = self.get_argument('dis_size', default=10, strip=True)
        name = self.get_argument('name', default = '', strip=True)
        artisans = artisan_service.search_artisan(page, dis_size, name, order_by, sort)
        self.render_json(artisans)
        
@application.RequestMapping("/api/artisan/([0-9]+)")
class Artisan(application.RequestHandler):
    @Api()
    def get(self, artisan_id):
        artisan = artisan_service.get_artisan(artisan_id)
        gallery = common_service.get_gallery(artisan_id, 'artisan')
        artisan.gallery = gallery
        self.render_json(artisan)
        
#######  SAMPLE ##################################
@application.RequestMapping("/api/tags")
class Tags(application.RequestHandler):
    @Api()
    def get(self):
        tags = sample_service.get_tags()
        self.render_json(tags)

@application.RequestMapping("/api/samples")
class Samples(application.RequestHandler):
    @Api()
    def get(self):
        order_by = self.get_argument('order_by', default='', strip=True)
        sort = self.get_argument('sort', default='asc', strip=True)
        page = self.get_argument('page', default=1, strip=True)
        dis_size = self.get_argument('dis_size', default=10, strip=True)
        artisan_id = self.get_argument('artisan_id', default='', strip=True)
        
        samples, hits = sample_service.search_sample(page, dis_size, artisan_id)
        self.render_json(samples)
     
@application.RequestMapping("/api/sample/([0-9]+)")
class Sample(application.RequestHandler):
    @Api()
    def get(self, sample_id):
        sample = sample_service.get_sample(sample_id)
        self.render_json(sample)