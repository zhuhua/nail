# -*- coding:utf-8 -*-
'''
Created on Jan 19, 2015

@author: zhuhua
'''
from simpletor.application import AppError
from simpletor.utils import md5
import models

gallery_types = {
    'artisan': 0,
    'user': 1,
    'sample': 2,
    'order': 3
}

counts_types = {
    'artisan': 0,
    'user': 1,
    'sample': 2,
    'order': 3
}

def add_to_gallery(obj_id, obj_type, url):
    '''添加图片到图库'''
    if not gallery_types.has_key(obj_type):
        raise AppError('类型错误')
    
    gallery_type = gallery_types[obj_type]
    obj_id = md5('%s_%s' % (obj_id, gallery_type))
    
    gallery = models.Gallery()
    gallery.obj_id = obj_id
    gallery.obj_type = gallery_type
    gallery.url = url
    models.galleryDAO.save(**gallery)
    
def remove_from_gallery(gallery_id):
    '''从图库删除图片'''
    models.galleryDAO.delete(gallery_id)
    
def remove_all(obj_id, obj_type):
    '''清空图库'''
    if not gallery_types.has_key(obj_type):
        raise AppError('类型错误')
    
    gallery_type = gallery_types[obj_type]
    obj_id = md5('%s_%s' % (obj_id, gallery_type))
    
    return models.galleryDAO.delete_all(obj_id)
    
def get_gallery(obj_id, obj_type):
    '''获取图片列表'''
    if not gallery_types.has_key(obj_type):
        raise AppError('类型错误')
    
    gallery_type = gallery_types[obj_type]
    obj_id = md5('%s_%s' % (obj_id, gallery_type))
    
    return models.galleryDAO.findByObjId(obj_id)

def update_count(obj_id, obj_type, key, value):
    '''更新计数'''
    if not counts_types.has_key(obj_type):
        raise AppError('类型错误')
    
    counts_type = counts_types[obj_type]
    obj_id = md5('%s_%s' % (obj_id, counts_type))
    
    counts = models.countsDAO.find(obj_id, key)
    if not counts:
        counts = models.Counts()
        counts.obj_id = obj_id
        counts.count_key = key
        counts.count_value = value
        models.countsDAO.save(**counts)
    else:
        counts.count_key = key
        counts.count_value = value
        models.countsDAO.update(**counts)
    
def get_counts(obj_id, obj_type):
    '''获取对象计数'''
    if not counts_types.has_key(obj_type):
        raise AppError('类型错误')
    
    counts_type = counts_types[obj_type]
    obj_id = md5('%s_%s' % (obj_id, counts_type))
    
    rows = models.countsDAO.findByObjId(obj_id)
    counts = dict()
    
    for row in rows:
        counts[row.count_key] = row.count_value
    return counts