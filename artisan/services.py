# -*- coding:utf-8 -*-
'''
Created on 2015-1-11

@author: Zhuhua
'''
import logging
import copy
from simpletor.torndb import transactional
from simpletor.application import AppError
from simpletor.tornsolr import index, connect, delete_index
from simpletor.tornredis import cacheable, cacheevict
from simpletor.utils import sha1, validate_utils
from datetime import datetime

from common import services as common_services
from sample import services as sample_services
import models

log = logging.getLogger(__name__)
artisan_count = {
    'sample': 0,
    'sale': 0,
    'evaluate_count': 0,
    'communication_rank': 50,
    'professional_rank': 50 ,
    'punctual_rank': 50,
    
}

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
def register(artisan):
            
    if validate_utils.is_empty_str(artisan.name):
        raise AppError('请填写姓名', field='name')
    
    if validate_utils.is_empty_str(artisan.mobile):
        raise AppError('请填写手机号', field='mobile')
    
    if not validate_utils.is_mobile(artisan.mobile):
        raise AppError('请填写正确的手机号', field='mobile')
        
    artisan_id = models.artisanDAO.save(**artisan)
    
    for k, v in artisan_count.iteritems():
        common_services.update_count(artisan_id, 'artisan', k, v)
    
    return get_artisan(artisan_id)
    
@transactional
def login(artisan_id, password):
    '''
    登录
    '''
    artisan = models.artisanDAO.find(artisan_id)
    if artisan is None:
        raise AppError('用户名错误', field = 'username')
    
    if artisan.password != sha1(password):
        raise AppError('密码错误', field = 'password')
    
    artisan.last_login = datetime.now()
    models.artisanDAO.update(**artisan)
    return artisan
    
@cacheable('#artisan_id', prefix='ARTISAN')
def get_artisan_from_db(artisan_id):
    artisan = models.artisanDAO.find(artisan_id)
    if artisan is None:
        raise AppError(u'该美甲师不存在')
    
    return artisan

def get_artisan(artisan_id):
                
    artisan = get_artisan_from_db(artisan_id)
    counts = common_services.get_counts(artisan_id, 'artisan')
    acounts = copy.copy(artisan_count)
    acounts.update(counts)
    artisan.counts = acounts
    
    return artisan

@transactional
@cacheevict('#artisan_id', prefix='ARTISAN')
def delelte_artisan(artisan_id):
    artisan = models.artisanDAO.find(artisan_id)
    artisan.status = 1
    models.artisanDAO.update(**artisan)
    sample_services.delete_sample_by_artisan(artisan_id)
    delete_index('artisan', 'id:%s' % artisan_id)
    
@index(core='artisan')
@transactional
@cacheevict('#artisan.id', prefix='ARTISAN')
def update_profile(artisan):
    validate_artisan(artisan)
    models.artisanDAO.update(**artisan)
    if artisan.counts != None:
        artisan_count.update(artisan.counts)
        
    for k, v in artisan_count.iteritems():
        common_services.update_count(artisan.id, 'artisan', k, v)
    
    return get_artisan(artisan.id)
    
def search_artisan(page=1, page_size=10, name='', order_by='create_time', sort='desc'):
    page = int(page)
    if page < 1:
        page = 1
    page_size = int(page_size)
    
    solr = connect(core='artisan')
    query = '*:*'
    if not name == '':
        query = 'name:%s' % name
        
    results = solr.search(query, **{
        'fq':'status:0',
        'start': (page - 1) * page_size,
        'rows': page_size,
        'sort': '%s %s' % (order_by, sort)
    })
    docs = results.docs
    artisans = []
    for doc in docs:
        try:
            artisans.append(get_artisan(doc['id']))
        except:
            log.debug('get artisan error %s' % doc['id'])
    return artisans, results.hits
    
@index(core='artisan')
@cacheevict('#artisan_id', prefix='ARTISAN')
def update_index(artisan_id):
    return get_artisan(artisan_id)
    