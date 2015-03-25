# -*- coding:utf-8 -*-
'''
Created on 2014年12月18日

@author: zhuhua
'''
from simpletor import application
from simpletor.utils import sha1, save_image, validate_utils

from backend import services as backend_service
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
        password = '123456'
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
        
        if not utils.checkcode.validate(mobile, password):
            raise application.AppError('验证码错误')
        
        user_service.register(mobile, password)
        token = user_service.login(mobile, password)
        self.render_json(token)
       
@application.RequestMapping("/api/user/profile") 
class UserProfile(application.RequestHandler):
    '''获取和修改用户信息'''
    @Api(auth=True)
    def get(self):
        user_id = self.user_id
        user = user_service.get_profile(user_id)
        user.pop('password')
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
        address.is_default = self.get_argument('is_default', default=0, strip=True)
        user_service.add_address(address)
        self.render_json(user_service.get_addresses(user_id))
        
@application.RequestMapping("/api/user/addresses")
class Addresses(application.RequestHandler):
    '''常用地址列表'''
    @Api(auth=True)
    def get(self):
        user_id = self.user_id
        self.render_json(user_service.get_addresses(user_id))

@application.RequestMapping("/api/user/address/default")
class DefaultAddress(application.RequestHandler):
    ''' 获取默认地址'''
    @Api(auth=True)
    def get(self):
        user_id = self.user_id
        self.render_json(user_service.get_default_address(user_id))
    '''设置常用地址为默认'''
        
    @Api(auth=True)
    def post(self):
        user_id = self.user_id
        address_id = self.get_argument('address_id', strip=True)
        user_service.set_default_address(user_id, address_id)
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
        self.render_json(artisans[0])
        
@application.RequestMapping("/api/artisan/([0-9]+)")
class Artisan(application.RequestHandler):
    '''获取美甲师信息'''
    @Api()
    def get(self, artisan_id):
        artisan = artisan_service.get_artisan(artisan_id)
        gallery = common_service.get_gallery(artisan_id, 'artisan')
        artisan.gallery = gallery
        self.render_json(artisan)

@application.RequestMapping("/api/my_mecat")
class MyArtisans(application.RequestHandler):
    '''我的大咖'''
    @Api()
    def get(self):
        user_id = self.user_id
        order_by = self.get_argument('order_by', default='create_time', strip=True)
        sort = self.get_argument('sort', default='desc', strip=True)
        page = self.get_argument('page', default=1, strip=True)
        page_size = self.get_argument('page_size', default=10, strip=True)
        artisans = artisan_service.my_artisan(user_id, page, page_size, order_by, sort)
        self.render_json(artisans[0])
        
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
        user_id = None
        try:
            user_id = self.user_id
        except:
            pass
        category_id = self.get_argument('category_id', default='1', strip=True)
        order_by = self.get_argument('order_by', default='create_time', strip=True)
        sort = self.get_argument('sort', default='desc', strip=True)
        page = self.get_argument('page', default=1, strip=True)
        page_size = self.get_argument('page_size', default=10, strip=True)
        artisan_id = self.get_argument('artisan_id', default='', strip=True)
        tag = self.get_argument('tag', default='', strip=True)
        
        result = sample_service.search_sample(category_id=category_id, page=page, page_size=page_size, \
                                              artisan_id=artisan_id, tag=tag, order_by=order_by, sort=sort)
        sids = list()
        sd = dict()
        res = result[0]
        for s in res:
            sd[s.id] = s
            sids.append(s.id)
            s.is_fav = 0
        
        fav_type = '2'
        if len(sids) > 1:
            favs = user_service.get_favorites_sub(user_id, fav_type, sids)
            fids = list()
            for fav in favs:
                fids.append(user_service.fav_types[fav_type](fav.object_id))
            for s in res:
                if s.id in fids:
                    s.is_fav = 1
        elif len(sids) == 1:
            fav = user_service.get_favorite(user_id, fav_type, sids[0])
            if fav is not None:
                res[0].is_fav = 1
                
        self.render_json(res)
     
@application.RequestMapping("/api/sample/([0-9]+)")
class Sample(application.RequestHandler):
    '''获取美甲师作品详情'''
    @Api()
    def get(self, sample_id):
        user_id = None
        try:
            user_id = self.user_id
        except:
            pass
        sample = sample_service.get_sample(sample_id)
        
        #添加收藏标记
        sample.is_fav = 0
        if user_id is not None:
            #查询用户有没有收藏这个样品
            fav = user_service.get_favorite(user_id, '2', sample.id)
            if fav is not None:
                sample.is_fav = 1
                
        self.render_json(sample)
        
@application.RequestMapping("/api/banners")
class Banners(application.RequestHandler):
    '''banner列表'''
    @Api()
    def get(self):
        banners = backend_service.get_banners()
        self.render_json(banners)
#         self.render('backend/api_banners.html', items=banners)
        
@application.RequestMapping("/api/banner/([0-9]+)")
class Banner(application.RequestHandler):
    '''banner 详情'''
    @Api()
    def get(self, banner_id):
        banner = backend_service.get_banner(banner_id)
        self.render('backend/api_banner.html', item=banner)
        
@application.RequestMapping("/api/user_agreement")
class UserAgreement(application.RequestHandler):
    '''用户协议'''
    @Api()
    def get(self):
        self.render('user_agreement.html')
        
@application.RequestMapping("/api/about_us")
class AboutUs(application.RequestHandler):
    '''关于我们'''
    @Api()
    def get(self):
        self.render('about_us.html')
        
@application.RequestMapping("/api/service_areas")
class ServiceAreas(application.RequestHandler):
    '''服务地区'''
    @Api()
    def get(self):
        self.render('service_areas.html')