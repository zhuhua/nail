# -*- coding:utf-8 -*-
'''
Created on Jan 20, 2015

@author: zhuhua
'''
from simpletor.torndb import transactional
from simpletor.application import AppError
from simpletor.tornsolr import index, connect
from simpletor.tornredis import cacheable, cacheevict
from simpletor.utils import validate_utils
from common import services as common_services

sample_count = {
    'sale': 0,
    'evaluate_count': 0,
}

import models

def get_categories():
    '''获取分类'''
    return models.categoryDAO.all()

def get_tags():
    '''获取标签'''
    return models.tagDAO.all()

def validate_sample(sample):
    '''表单验证'''
    if validate_utils.is_empty_str(sample.name):
        raise AppError('请填写名称', field='name')
    
    if validate_utils.is_empty_str(sample.tag_price):
        raise AppError('请填写店面价', field='tag_price')
    
    try:
        float(sample.tag_price)
    except:
        raise AppError('店面价为小数', field='tag_price')
    
    if validate_utils.is_empty_str(sample.price):
        raise AppError('请填写价格', field='price')
    
    try:
        float(sample.tag_price)
    except:
        raise AppError('价格为小数', field='price')
    
    if validate_utils.is_empty_str(sample.brief):
        raise AppError('请填写描述', field='brief')
    
    if len(sample.images) == 0:
        raise AppError('至少上传一张图片', field='images')

@index(core='sample')
@transactional
def add_sample(sample):
    '''发布作品'''
    validate_sample(sample)
    images = sample.images

    sample_id = models.sampleDAO.save(**sample)
    for image in images:
        common_services.add_to_gallery(sample_id, 'sample', image)
        
    for k, v in sample_count.iteritems():
        common_services.update_count(sample_id, 'sample', k, v)
    
    return get_sample(sample_id)
        

def get_sample(sample_id):
    '''获取作品'''
    
    sample = get_sample_from_db(sample_id)
    counts = common_services.get_counts(sample_id, 'sample')
    
    sample_count.update(counts)
    sample.counts = sample_count
        
    return sample

@cacheable('#sample_id', prefix='SAMPLE')
def get_sample_from_db(sample_id):
    sample = models.sampleDAO.find(sample_id)
    if sample is None:
        raise AppError(u'该作品不存在')
    
    images = common_services.get_gallery(sample_id, 'sample')
    sample.images = images
    sample.tags = sample.tags.split(' ')
    
    return sample

@index(core='sample')
@transactional
@cacheevict('#sample.id', prefix='SAMPLE')
def update_sample(sample):
    '''编辑作品'''
    sample_id = sample.id
    if isinstance(sample.tags, list):
        sample.tags = ' '.join(sample.tags)
    models.sampleDAO.update(**sample)
    
    images = sample.images
    common_services.remove_all(sample_id, 'sample')
    for image in images:
        common_services.add_to_gallery(sample_id, 'sample', image)
        
    for k, v in sample.counts.iteritems():
        common_services.update_count(sample.id, 'sample', k, v)
        
    return get_sample(sample_id)

def search_sample(page=1, page_size=10, category_id='*', artisan_id='', tag='', order_by='create_time', sort='desc'):
    page = int(page)
    page_size = int(page_size)
    
    solr = connect(core='sample')
    query = 'status:0' % category_id
    if not category_id == '':
        query += 'AND category_id:%s' % category_id
        
    if not artisan_id == '':
        query += ' AND artisan_id:%s' % artisan_id
        
    if not tag == '':
        query += ' AND tags:%s' % tag
        
    results = solr.search(query, **{
        'start': (page - 1) * page_size,
        'rows': page_size,
        'sort': '%s %s' % (order_by, sort)
    })
    
    docs = results.docs
    samples = [get_sample(doc['id']) for doc in docs]
    return samples, results.hits

@index(core='sample')
@cacheevict('#sample_id', prefix='SAMPLE')
def update_sample_index(sample_id):
    return get_sample(sample_id)