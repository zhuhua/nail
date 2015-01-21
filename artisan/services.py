# -*- coding:utf-8 -*-
'''
Created on 2015-1-11

@author: Zhuhua
'''
from simpletor.torndb import transactional
from simpletor.application import AppError
from simpletor.utils import sha1
from datetime import datetime

import models

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
        
    models.artisanDAO.save(artisan)
    
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
    models.artisanDAO.update(artisan)
    return artisan
    
def get(artisan_id):
    return models.artisanDAO.find(artisan_id)
    
@transactional
def update_profile(artisan_id, **profile):
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
    
    models.artisanDAO.update(**artisan)
    
def paging(page, size):
    artisan = models.artisanDAO.paging(0, 10)
    return artisan
    