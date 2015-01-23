# -*- coding:utf-8 -*-
'''
Created on Jan 20, 2015

@author: zhuhua
'''
from simpletor.torndb import transactional
from simpletor.application import AppError
from simpletor.tornsolr import index
from common import services as common_serv
import models

def get_categories():
    '''获取分类'''
    return models.categoryDAO.all()

def get_tags():
    '''获取标签'''
    return models.tagDAO.all()


@index(core='sample')
@transactional
def add_sample(sample):
    '''发布作品'''
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
    return sample
        
@index(core='sample')
@transactional
def update_sample(sample_id, sample):
    '''编辑作品'''
    models.sampleDAO.update(sample)
    
    images = sample.images
    common_serv.remove_all(sample_id, 'sample')
    for image in images:
        common_serv.add_to_gallery(sample_id, 'sample', image)
        
    return get_sample(sample_id) 
