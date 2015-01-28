# -*- coding:utf-8 -*-
'''
Created on 2014年12月18日

@author: zhuhua
'''
from simpletor import application
from simpletor.utils import sha1, save_image

from user import services as user_service
from artisan import services as artisan_service
from sample import services as sample_service
from common import services as common_service
from api import Api

#######  USER ##################################
@application.RequestMapping("/api/user/register")
class Register(application.RequestHandler):
    '''注册'''
    @Api()
    def post(self):
        mobile = self.get_argument('mobile', strip=True)
        password = self.get_argument('password', strip=True)
        checkcode = self.get_argument('checkcode', strip=True)
        
        if not checkcode == '111111':
            raise application.AppError('验证码错误')
        
        user_service.register(mobile, password)
        self.finish()

@application.RequestMapping("/api/user/login")
class Login(application.RequestHandler):
    '''登录'''
    @Api()
    def post(self):
        mobile = self.get_argument('mobile', strip=True)
        password = self.get_argument('password', strip=True)
        token = user_service.login(mobile, password)
        self.render_json(token)
       
@application.RequestMapping("/api/user/profile") 
class UserProfile(application.RequestHandler):
    '''获取和修改用户信息'''
    @Api(auth=True)
    def get(self):
        user_id = self.user_id
        user = user_service.get_profile(user_id)
        self.render_json(user)
    
    @Api(auth=True)
    def post(self):
        user_id = self.user_id
        user = user_service.get_profile(user_id)
        user.nick = self.get_argument('nick', '', strip=True)
        user_service.update_profile(user)
        self.render_json(user)
        
@application.RequestMapping("/api/user/passwd") 
class ChangePwd(application.RequestHandler):
    '''更改密码'''
    @Api(auth=True)
    def post(self):
        user_id = self.user_id
        user = user_service.get_profile(user_id)
        
        old_pwd = self.get_argument('old_pwd', strip=True)
        password = self.get_argument('password', strip=True)
                
        if not user.password == sha1(old_pwd):
            raise application.AppError(u'原密码不正确')
        
        user.password = password
        user_service.update_profile(user)
        self.render_json(user)
        
@application.RequestMapping("/api/user/avatar")
class UploadAvatar(application.RequestHandler):
    '''上传头像'''
    @Api(auth=True)
    def post(self):
        user_id = self.user_id
        file_dict_list = self.request.files['file']
        filename = ''
        for file_dict in file_dict_list:
            filename = file_dict["filename"]
            filename = save_image(filename, file_dict["body"])
        
        user = user_service.get_profile(user_id)
        user.avatar = "/img/%s" % filename
        user_service.update_profile(user)
        self.render_json(user)
        
#######  ARTISAN ##################################
@application.RequestMapping("/api/artisans")
class Artisans(application.RequestHandler):
    '''获取美甲师列表'''
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
    '''获取美甲师信息'''
    @Api()
    def get(self, artisan_id):
        artisan = artisan_service.get_artisan(artisan_id)
        gallery = common_service.get_gallery(artisan_id, 'artisan')
        artisan.gallery = gallery
        self.render_json(artisan)
        
#######  SAMPLE ##################################
@application.RequestMapping("/api/tags")
class Tags(application.RequestHandler):
    '''获取标签列表'''
    @Api()
    def get(self):
        tags = sample_service.get_tags()
        self.render_json(tags)

@application.RequestMapping("/api/samples")
class Samples(application.RequestHandler):
    '''获取美甲师作品列表'''
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
    '''获取美甲师作品详情'''
    @Api()
    def get(self, sample_id):
        sample = sample_service.get_sample(sample_id)
        self.render_json(sample)