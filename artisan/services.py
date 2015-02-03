# -*- coding:utf-8 -*-
'''
Created on 2015-1-11

@author: Zhuhua
'''
from simpletor.torndb import transactional
from simpletor.application import AppError
from simpletor.tornsolr import index, connect
from simpletor.tornredis import cacheable, cacheevict
from simpletor.utils import sha1, validate_utils
from datetime import datetime

import models

def validate_artisan(artisan):
    '''Artisan 表单验证'''
    if validate_utils.is_empty_str(artisan.name):
        raise AppError('请填写姓名', field='name')
    
    if validate_utils.is_empty_str(artisan.mobile):
        raise AppError('请填写手机号', field='mobile')
    
    if not validate_utils.is_mobile(artisan.mobile):
        raise AppError('请填写正确的手机号', field='mobile')
    
    if validate_utils.is_empty_str(artisan.serv_area):
        raise AppError('请填写服务区域', field='serv_area')
    
@index(core='artisan')
@transactional
def register(name, mobile, password, **profile):
    artisan = models.Artisan()
    artisan.name = name
    artisan.password = sha1(password)
    artisan.mobile = mobile
    artisan.gender = profile.pop('gender', 1)
    
    avatar = profile.pop('avatar', None)
    brief = profile.pop('brief', None)
    
    if avatar:
        artisan.avatar = avatar
    if brief:
        artisan.brief = brief
        
    artisan_id = models.artisanDAO.save(**artisan)
    return get_artisan(artisan_id)
    
@transactional
def login(artisan_id, password):
    '''
    登录
    '''
    artisan = models.artisanDAO.find(artisan_id)
    if artisan is None:
        raise AppError('用户名错误')
    
    if artisan.password != sha1(password):
        raise AppError('密码错误')
    
    artisan.last_login = datetime.now()
    models.artisanDAO.update(**artisan)
    return artisan
    
@cacheable('#artisan_id', prefix='ARTISAN')
def get_artisan(artisan_id):
    return models.artisanDAO.find(artisan_id)
    
@cacheevict('#artisan.id', prefix='ARTISAN')
@index(core='artisan')
@transactional
def update_profile(artisan):
    validate_artisan(artisan)
    models.artisanDAO.update(**artisan)
    return get_artisan(artisan.id)
    
def search_artisan(page=1, dis_size=10, name='', order_by='', sort='asc'):
    solr = connect(core='artisan')
    query = '*:*'
    if not name == '':
        query = 'name:%s' % name
    
    results = solr.search(query)
    docs = results.docs
    samples = [get_artisan(doc['id']) for doc in docs]
    return samples, results.hits
    