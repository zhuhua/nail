# -*- coding:utf-8 -*-
'''
Created on 2015-1-11

@author: Zhuhua
'''
from simpletor.torndb import transactional
from simpletor.application import AppError
from simpletor.tornsolr import index, connect
from simpletor.utils import sha1
from datetime import datetime

import models

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
    
def get_artisan(artisan_id):
    return models.artisanDAO.find(artisan_id)
    
@index(core='artisan')
@transactional
def update_profile(profile):
    artisan_id = profile['id']
    artisan = models.artisanDAO.find(artisan_id)
    if not artisan:
        return
    
    name = profile.pop('name', None)
    gender = profile.pop('gender', 1)
    avatar = profile.pop('avatar', None)
    brief = profile.pop('brief', None)
    
    if name:
        artisan.name = name
    if gender:
        artisan.gender = int(gender)
    if avatar:
        artisan.avatar = avatar
    if brief:
        artisan.brief = brief
        
    if artisan.last_login is None:
        artisan.last_login = datetime.now()
    
    models.artisanDAO.update(**artisan)
    return get_artisan(artisan_id)
    
def search_artisan(page=1, dis_size=10, name='', order_by='', sort='asc'):
    solr = connect(core='artisan')
    query = '*:*'
    if not name == '':
        query = 'name:%s' % name
    
    results = solr.search(query)
    docs = results.docs
    samples = [get_artisan(doc['id']) for doc in docs]
    return samples, results.hits
    