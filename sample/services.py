# -*- coding:utf-8 -*-
'''
Created on Jan 20, 2015

@author: zhuhua
'''
from simpletor.torndb import transactional
from simpletor.application import AppError
from simpletor.tornsolr import index, connect
from simpletor.utils import validate_utils
from common import services as common_serv
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
        common_serv.add_to_gallery(sample_id, 'sample', image)
    
    return get_sample(sample_id)
        
def get_sample(sample_id):
    '''获取作品'''
    sample = models.sampleDAO.find(sample_id)
    images = common_serv.get_gallery(sample_id, 'sample')
    sample.images = images
    sample.tags = sample.tags.split(' ')
    return sample
        
@index(core='sample')
@transactional
def update_sample(sample):
    '''编辑作品'''
    sample_id = sample.id
    models.sampleDAO.update(**sample)
    
    images = sample.images
    common_serv.remove_all(sample_id, 'sample')
    for image in images:
        common_serv.add_to_gallery(sample_id, 'sample', image)
        
    return get_sample(sample_id)

def search_sample(category_id, page=1, dis_size=10, artisan_id='', order_by='', sort='asc'):
    solr = connect(core='sample')
    query = 'category_id:%s' % category_id
    if not artisan_id == '':
        query += 'AND artisan_id:%s' % artisan_id
    
    results = solr.search(query)
    docs = results.docs
    samples = [get_sample(doc['id']) for doc in docs]
    return samples, results.hits