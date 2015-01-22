# -*- coding:utf-8 -*-
'''
<<<<<<< HEAD
Created on Jan 20, 2015

@author: zhuhua
'''
from simpletor.torndb import transactional
from simpletor.application import AppError
from common import services as common_serv
import models

def get_categories():
    '''获取分类'''
    return models.categoryDAO.all()

@transactional
def add_sample(sample):
    '''发布作品'''
    images = sample.images
    
    sample_id = models.sampleDAO.save(sample)
    
    for image in images:
        common_serv.add_to_gallery(sample_id, 'sample', image)
        
def get_sample(sample_id):
    '''获取作品'''
    sample = models.sampleDAO.find(sample_id)
        
def update_sample(sample_id, sample):
    '''编辑作品'''
    models.sampleDAO.update(sample)
    
    images = sample.images
    common_serv.remove_all(sample_id, 'sample')
    for image in images:
        common_serv.add_to_gallery(sample_id, 'sample', image)
