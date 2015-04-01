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
from simpletor.utils import validate_utils

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
    validate_banner(banner)
    banner.detail = json.dumps(banner.detail)
    models.bannerDAO.save(**banner)
    banners = get_banners()
    
    return banners

@transactional
def edit_banner(banner):
    #validate
    validate_banner(banner)
    bannerr = models.bannerDAO.find(banner.id)
    if bannerr is None:
        raise AppError('banner not exist')
    bannerr.name = banner.name
    bannerr.cover = banner.cover
    bannerr.url = banner.url
    bannerr.detail = json.dumps(banner.detail)
    models.bannerDAO.update(**bannerr)
    
def validate_banner(banner):
    if validate_utils.is_empty_str(banner.name):
        raise AppError('请填写名称', field='name')
    if validate_utils.is_empty_str(banner.cover):
        raise AppError('上传Banner图', field='cover')
    if validate_utils.is_empty_str(banner.url):
        raise AppError('请填写URL', field='url')
    
    if len(banner.detail) < 2:
        raise AppError('请填写详情', field='image1')
    if validate_utils.is_empty_str(banner.detail[0]['image']):
        raise AppError('请填上传图片', field='image1')
    if validate_utils.is_empty_str(banner.detail[1]['image']):
        raise AppError('请填上传图片', field='image2')
    if validate_utils.is_empty_str(banner.detail[0]['description']):
        raise AppError('请填写详情', field='description1')
    if validate_utils.is_empty_str(banner.detail[1]['description']):
        raise AppError('请填写详情', field='description2')