# -*- coding:utf-8 -*-
'''
Created on 2014-12-23

@author: zhuhua
'''
from uuid import uuid4
from datetime import datetime
from simpletor.torndb import transactional
from simpletor.application import AppError
from simpletor.utils import sha1, validate_utils

from artisan import services as artisan_serv
from sample import services as sample_serv

import time
import models

@transactional
def register(mobile, password):
    '''User Register'''
    if not validate_utils.is_mobile(mobile):
        raise AppError(u'请填写正确的手机号' % mobile, field='mobile')
    
    user = models.userDAO.findByMobile(mobile)
    if user is not None:
#         raise AppError(u'手机号%s已存在' % mobile, field='mobile')
        return user

    user = models.User()
    user.mobile = mobile
    user.nick = mobile
    user.password = sha1(password)
    
    models.userDAO.save(**user)
    return user

@transactional
def login(mobile, password):
    '''Login'''
    user = models.userDAO.findByMobile(mobile)
    if user is None:
        raise AppError(u'手机号不存在', field='mobile')
    
#     if user.password != sha1(password):
#         raise AppError(u'密码错误', field='password')
    
    user_id = user.id
    token = models.loginTokenDAO.findByUser(user_id)
    
    if token is None:
        token = models.LoginToken()
        token.user_id = user_id
        models.loginTokenDAO.save(**token)
    else:
        token.token = uuid4().hex
        token.expire = time.time() + 86400 * 30
        token.last_login = datetime.now()
        models.loginTokenDAO.update(**token)
        
    return token

@transactional
def update_profile(user):
    '''更新用户信息'''
    if validate_utils.is_empty_str(user.nick):
        raise AppError(u'请填写昵称', field='nick')
    
    models.userDAO.update(**user)

def get_token(token):
    return models.loginTokenDAO.find(token)

def get_profile(user_id):
    user = models.userDAO.find(user_id)
    return user

@transactional
def add_address(address):
    '''添加常用地址'''
    if validate_utils.is_empty_str(address.location):
        raise AppError(u'请选择位置', field='location')
    
    if validate_utils.is_empty_str(address.detail):
        raise AppError(u'请填写详细地址', field='detail')
    if int(address.is_default) == 1:
        user_id = address.user_id
        default_addr = models.addressDAO.find_default(user_id)
        if default_addr != None:
            models.addressDAO.change_default(0, default_addr.id, user_id);
    models.addressDAO.save(**address)
    
def get_addresses(user_id):
    '''常用地址列表'''
    return models.addressDAO.find_by_user(user_id)

@transactional
def set_default_address(user_id, address_id):
    '''设置常用地址为默认'''
    default_addr = models.addressDAO.find_default(user_id)
    if default_addr != None:
        if default_addr.user_id != user_id:
            raise AppError(u'地址不属于此用户')
        if default_addr.id != address_id:
            models.addressDAO.change_default(0, default_addr.id, user_id);
    addr = models.addressDAO.find(address_id)
    if addr.user_id != user_id:
            raise AppError(u'地址不属于此用户')
    models.addressDAO.change_default(1, address_id, user_id);

def get_default_address(user_id):
    default_addr = models.addressDAO.find_default(user_id)
    if default_addr == None:
        addrs = models.addressDAO.find_by_user(user_id)
        if len(addrs) > 0:
            sda = addrs[0]
            models.addressDAO.change_default(1, sda.id, sda.user_id);
        default_addr = models.addressDAO.find_default(user_id)
    
    return default_addr

@transactional
def del_address(user_id, address_id):
    '''删除常用地址'''
    address = models.addressDAO.find(address_id)
    if not address.user_id == user_id:
        raise AppError(u'没有权限删除')
    models.addressDAO.delete(address_id)
    
fav_types = {
    '1': int, #美甲师
    '2': int #美甲作品
}
    
@transactional
def add_favorite(favorite):
    '''添加收藏'''
    if validate_utils.is_empty_str(favorite.object_id):
        raise AppError(u'没有收藏对象', field='object_id')

    if not favorite.type in fav_types.keys():
        raise AppError(u'类型错误')
    
    try:
        favorite.object_id = fav_types[favorite.type](favorite.object_id)
    except Exception:
        raise AppError(u'收藏对象有误')
    
    try:
        if favorite.type == '1':
            artisan_serv.get_artisan(favorite.object_id)
        elif favorite.type == '2':
            sample_serv.get_sample(favorite.object_id)
    except AppError, e:
        raise e
    
   
    if models.favoriteDAO.find_by_object(**favorite) is not None:
            raise AppError(u'该收藏已存在')
        
    if favorite.type == '1':
        #查看是否有删除状态
        favorite.status = 1
        old_fav = models.favoriteDAO.find_by_object(**favorite);
        if old_fav is not None:
            old_fav.update_time = datetime.now()
            old_fav.status = 0
            models.favoriteDAO.update(**old_fav)
            return
        else:
            favorite.status = 0
    models.favoriteDAO.save(**favorite)
    
def get_favorites(user_id, fav_type, page=1, page_size=10):
    '''收藏列表'''
    if not fav_type in fav_types.keys():
        raise AppError(u'类型错误')
        
    page = int(page)
    page_size = int(page_size)
    offset = (page - 1) * page_size
    status = 0
    results = models.favoriteDAO.find_by_user(user_id, fav_type, status, page_size, offset)
    objects = []
    for row in results:
        object_id = fav_types[fav_type](row.object_id)
        if fav_type == '1':
            objects.append(artisan_serv.get_artisan(object_id))
        elif fav_type == '2':
            objects.append(sample_serv.get_sample(object_id))
            
    return objects

def get_favorite(user_id, fav_type, object_id):
    '''收藏对象'''
    if not fav_type in fav_types.keys():
        raise AppError(u'类型错误')
    favorite = models.Favorite()
    favorite.user_id = user_id
    favorite.type = fav_type
    favorite.object_id = object_id
    fav = models.favoriteDAO.find_by_object(**favorite)
    
    return fav

def get_favorites_sub(user_id, fav_type, object_ids):
    '''指定对象的收藏对象'''
    if not fav_type in fav_types.keys():
        raise AppError(u'类型错误')
    status = 0
    favs = models.favoriteDAO.find_by_user_objects(user_id, fav_type, object_ids, status)
    
    return favs

@transactional
def del_favorite(user_id, favorite):
    '''删除收藏'''
    favorite = models.favoriteDAO.find_by_object(**favorite)
    if favorite is None:
        raise AppError(u'收藏不存在')
    
    fav_type = favorite.type
    if not favorite.user_id == user_id:
        raise AppError(u'没有权限删除')
    
    favorite.status = 1
    models.favoriteDAO.update(**favorite)
    return fav_type
