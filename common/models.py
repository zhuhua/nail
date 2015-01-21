# -*- coding:utf-8 -*-
'''
Created on Jan 19, 2015

@author: zhuhua
'''
import time
from datetime import datetime
from simpletor.torndb import torndb, Row

class Gallery(Row):
    '''
    图库
    '''
    def __init__(self):
        self.id = None
        self.obj_id = None
        self.url = None
        self.create_time = datetime.now()
        
class GalleryDAO:
    '''
    图库数据接口
    '''
    def save(self, gallery):
        sql = '''
        INSERT INTO gallery (obj_id, url, create_time) 
        VALUES (%(obj_id)s, %(url)s, %(create_time)s)
        '''
        torndb.execute(sql, **gallery)
        
    def find(self, gallery_id):
        sql = '''
        SELECT * FROM gallery g WHERE g.id = %s
        '''
        return torndb.get(sql, gallery_id)
    
    def delete(self, gallery_id):
        sql = '''
        DELETE FROM gallery g WHERE g.id = %s
        '''
        return torndb.get(sql, gallery_id)
        
    def findByObjId(self, obj_id):
        sql = '''
        SELECT * FROM gallery g WHERE g.obj_id = %s ORDER BY g.create_time DESC
        '''
        return torndb.query(sql, obj_id)
    
    def delete_all(self, obj_id):
        sql = '''
        DELETE FROM gallery g WHERE g.obj_id = %s
        '''
        return torndb.get(sql, obj_id)
        
galleryDAO = GalleryDAO()

class Counts(Row):
    '''
    通用计数
    '''
    def __init__(self):
        self.id = None
        self.obj_id = None
        self.key = None
        self.value = 0
        self.version = time.time()
        
class CountsDAO:
    '''
    通用计数数据访问接口
    '''
    def save(self, counts):
        sql = '''
        INSERT INTO counts (obj_id, key, value, version) 
        VALUES (%(obj_id)s, %(key)s, %(value)s, %(version)s);
        '''
        torndb.execute(sql, **counts)
        
    def find(self, obj_id, key):
        sql = '''
        SELECT * FROM count c WHERE c.obj_id = %s AND c.key = %s;
        '''
        return torndb.get(sql, obj_id, key)
    
    def findByObjId(self, obj_id):
        sql = '''
        SELECT * FROM count c WHERE c.obj_id = %s;
        '''
        return torndb.query(sql, obj_id)
    
    def update(self, counts):
        sql = '''
        UPDATE counts c 
        SET value = value + %(value)s 
        WHERE c.obj_id = %(obj_id)s AND c.key = %(key)s;
        '''
        torndb.execute(sql, **counts)
        
countsDAO = CountsDAO()