# -*- coding:utf-8 -*-
'''
Created on Jan 15, 2015

@author: zhuhua
'''
import models
import json

from datetime import datetime
from simpletor.application import AppError
from simpletor.utils import sha1
from simpletor.torndb import transactional

@transactional
def login(username, password):
    '''
    登录
    '''
    manager = models.managerDAO.findByName(username)
    if manager is None:
        raise AppError('用户名错误')
    
    if manager.password != sha1(password):
        raise AppError('密码错误')
    
    manager.last_login = datetime.now()
    models.managerDAO.update(**manager)
    return manager

def build_detail(detail):
    detail = json.loads(detail)
    detail = sorted(detail, key = lambda item:item['serial_number'])
    return detail

def get_banners():
    '''
    banner 活动列表
    '''
    banners = models.bannerDAO.find_all()
    for banner in banners:
       
        banner.detail = build_detail(banner.detail)
    banners = sorted(banners, key = lambda banner: banner['serial_number'] )
    return banners

def get_banner(banner_id):
    '''
    banner 活动详情
    '''
    banner = models.bannerDAO.find(banner_id)
    banner.detail = build_detail(banner.detail)
    return banner
    
@transactional
def add_banner(banner):
    '''
    添加活动banner
    '''
    banner.detail = json.dumps(banner.detail)
    models.bannerDAO.save(**banner)
    banners = get_banners()
    
    return banners