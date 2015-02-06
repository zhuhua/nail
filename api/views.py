# -*- coding:utf-8 -*-
'''
Created on 2014年12月18日

@author: zhuhua
'''
from simpletor import application
from simpletor.utils import sha1, save_image, validate_utils

from user import services as user_service
from artisan import services as artisan_service
from sample import services as sample_service
from common import services as common_service
from api import Api
import utils

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
        
@application.RequestMapping("/api/user/checkcode")
class Checkcode(application.RequestHandler):
    '''注册'''
    @Api()
    def post(self):
        mobile = self.get_argument('mobile', strip=True)
        if not validate_utils.is_mobile(mobile):
            raise application.AppError(u'请填写正确的手机号' % mobile, field='mobile')
        
        utils.checkcode.send(mobile)
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
        
@application.RequestMapping("/api/user/address")
class AddAddress(application.RequestHandler):
    '''添加常用地址'''
    @Api(auth=True)
    def post(self):
        user_id = self.user_id
        address = user_service.models.Address()
        address.user_id = user_id
        address.location = self.get_argument('location', strip=True)
        address.detail = self.get_argument('detail', strip=True)
        user_service.add_address(address)
        self.render_json(user_service.get_addresses(user_id))
        
@application.RequestMapping("/api/user/addresses")
class Addresses(application.RequestHandler):
    '''常用地址列表'''
    @Api(auth=True)
    def get(self):
        user_id = self.user_id
        self.render_json(user_service.get_addresses(user_id))
        
@application.RequestMapping("/api/user/address/([0-9]+)")
class DelAddress(application.RequestHandler):
    '''删除常用地址'''
    @Api(auth=True)
    def post(self, address_id):
        user_id = self.user_id
        user_service.del_address(user_id, address_id)
        self.render_json(user_service.get_addresses(user_id))
        
@application.RequestMapping("/api/user/favorite")
class AddFavorite(application.RequestHandler):
    '''添加收藏'''
    @Api(auth=True)
    def post(self):
        user_id = self.user_id
        favorite = user_service.models.Favorite()
        favorite.user_id = user_id
        fav_type = self.get_argument('type', strip=True)
        favorite.type = fav_type
        favorite.object_id = self.get_argument('object_id', strip=True)
        user_service.add_favorite(favorite)
        self.render_json(user_service.get_favorites(user_id, fav_type))
        
@application.RequestMapping("/api/user/favorites")
class Favorites(application.RequestHandler):
    '''收藏列表'''
    @Api(auth=True)
    def get(self):
        user_id = self.user_id
        fav_type = self.get_argument('type', strip=True)
        page = int(self.get_argument('page', strip=True))
        page_size = int(self.get_argument('page_size', strip=True))
        self.render_json(user_service.get_favorites(user_id, fav_type, page, page_size))
        
@application.RequestMapping("/api/user/favorite/delete")
class DelFavorite(application.RequestHandler):
    '''删除收藏'''
    @Api(auth=True)
    def post(self):
        user_id = self.user_id
        favorite = user_service.models.Favorite()
        favorite.user_id = user_id
        fav_type = self.get_argument('type', strip=True)
        favorite.type = fav_type
        favorite.object_id = self.get_argument('object_id', strip=True)
        user_service.del_favorite(user_id, favorite)
        self.render_json(user_service.get_favorites(user_id, fav_type))
        
#######  ARTISAN ##################################
@application.RequestMapping("/api/artisans")
class Artisans(application.RequestHandler):
    '''获取美甲师列表'''
    @Api()
    def get(self):
        order_by = self.get_argument('order_by', default='create_time', strip=True)
        sort = self.get_argument('sort', default='asc', strip=True)
        page = self.get_argument('page', default=1, strip=True)
        page_size = self.get_argument('page_size', default=10, strip=True)
        name = self.get_argument('name', default = '', strip=True)
        artisans = artisan_service.search_artisan(page, page_size, name, order_by, sort)
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
        
@application.RequestMapping("/api/categories")
class Categories(application.RequestHandler):
    '''获取分类列表'''
    @Api()
    def get(self):
        categories = sample_service.get_categories()
        self.render_json(categories)

@application.RequestMapping("/api/samples")
class Samples(application.RequestHandler):
    '''获取美甲师作品列表'''
    @Api()
    def get(self):
        category_id = self.get_argument('category_id', default='1', strip=True)
        order_by = self.get_argument('order_by', default='create_time', strip=True)
        sort = self.get_argument('sort', default='desc', strip=True)
        page = self.get_argument('page', default=1, strip=True)
        page_size = self.get_argument('page_size', default=10, strip=True)
        artisan_id = self.get_argument('artisan_id', default='', strip=True)
        tag = self.get_argument('tag', default='', strip=True)
        
        result = sample_service.search_sample(category_id=category_id, page=page, page_size=page_size, \
                                              artisan_id=artisan_id, tag=tag, order_by=order_by, sort=sort)
        self.render_json(result[0])
     
@application.RequestMapping("/api/sample/([0-9]+)")
class Sample(application.RequestHandler):
    '''获取美甲师作品详情'''
    @Api()
    def get(self, sample_id):
        sample = sample_service.get_sample(sample_id)
        self.render_json(sample)