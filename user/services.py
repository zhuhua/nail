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
        raise AppError(u'手机号%s已存在' % mobile, field='mobile')

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
    
    if user.password != sha1(password):
        raise AppError(u'密码错误', field='password')
    
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
        raise AppError('请填写昵称', field='nick')
    
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
        raise AppError('请选择位置', field='location')
    
    if validate_utils.is_empty_str(address.detail):
        raise AppError('请填写详细地址', field='detail')
    
    models.addressDAO.save(**address)
    
def get_addresses(user_id):
    '''常用地址列表'''
    return models.addressDAO.find_by_user(user_id)

@transactional
def del_address(user_id, address_id):
    '''删除常用地址'''
    address = models.addressDAO.find(address_id)
    if not address.user_id == user_id:
        raise AppError('没有权限删除')
    models.addressDAO.delete(address_id)
    
fav_types = {
    1: int, #美甲师
    2: int #美甲作品
}
    
@transactional
def add_favorite(favorite):
    '''添加收藏'''
    if validate_utils.is_empty_str(favorite.objetc_id):
        raise AppError('没有收藏对象', field='objetc_id')

    if favorite.type not in fav_types.keys():
        raise AppError('类型错误')
    
    try:
        favorite.objetc_id = fav_types[favorite.type](favorite.objetc_id)
    except:
        raise AppError('收藏对象有误')
    
    models.favoriteDAO.save(**favorite)
    
def get_favorites(user_id, fav_type, page=1, page_size=10):
    '''收藏列表'''
    try:
        fav_type = int(fav_type)
    except:
        raise AppError('类型错误')
        
    offset = (page - 1) * page_size
    results = models.addressDAO.find_by_user(user_id, fav_type, page_size, offset)
    objects = []
    for object_id in results:
        object_id = fav_types[fav_type](object_id)
        if fav_type == 1:
            objects.append(artisan_serv.get_artisan(object_id))
        elif fav_type == 2:
            objects.append(sample_serv.get_sample(object_id))
    return objects
    
@transactional
def del_favorite(user_id, favorite_id):
    '''删除常用地址'''
    favorite = models.favoriteDAO.find(favorite_id)
    fav_type = favorite.type
    if not favorite.user_id == user_id:
        raise AppError('没有权限删除')
    models.favoriteDAO.delete(favorite_id)
    return fav_type
