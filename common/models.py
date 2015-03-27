# -*- coding:utf-8 -*-
'''
Created on Jan 19, 2015

@author: zhuhua
'''
from datetime import datetime
from simpletor import torndb

class Gallery(torndb.Row):
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
    @torndb.insert
    def save(self, **gallery):
        sql = '''
        INSERT INTO gallery (obj_id, url, create_time) 
        VALUES (%(obj_id)s, %(url)s, %(create_time)s)
        '''
        return sql
        
    @torndb.get
    def find(self, gallery_id):
        sql = '''
        SELECT * FROM gallery g WHERE g.id = %s
        '''
        return sql
    
    @torndb.delete
    def delete(self, gallery_id):
        sql = '''
        DELETE FROM gallery WHERE id = %s
        '''
        return sql
        
    @torndb.select
    def findByObjId(self, obj_id):
        sql = '''
        SELECT * FROM gallery g WHERE g.obj_id = %s ORDER BY g.create_time DESC
        '''
        return sql
    
    @torndb.delete
    def delete_all(self, obj_id):
        sql = '''
        DELETE FROM gallery WHERE obj_id = %s;
        '''
        return sql
        
galleryDAO = GalleryDAO()

class Counts(torndb.Row):
    '''
    通用计数
    '''
    def __init__(self):
        self.id = None
        self.obj_id = None
        self.count_key = None
        self.count_value = 0
        self.version = datetime.now()
        
class CountsDAO:
    '''
    通用计数数据访问接口
    '''
    @torndb.insert
    def save(self, **counts):
        sql = '''
        INSERT INTO counts(obj_id, count_key, count_value, version) 
        VALUES (%(obj_id)s, %(count_key)s, %(count_value)s, %(version)s);
        '''
        return sql
        
    @torndb.get
    def find(self, obj_id, key):
        sql = '''
        SELECT * FROM counts c WHERE c.obj_id = %s AND c.count_key = %s;
        '''
        return sql
    
    @torndb.get
    def find_by_id(self, count_id):
        sql = '''
        SELECT * FROM counts c WHERE c.id = %s;
        '''
        return sql
    
    @torndb.select
    def findByObjId(self, obj_id):
        sql = '''
        SELECT c.id FROM counts c WHERE c.obj_id = %s;
        '''
        return sql
    
    @torndb.update
    def update(self, **counts):
        sql = '''
        UPDATE counts c 
        SET count_value = %(count_value)s 
        WHERE c.obj_id = %(obj_id)s AND c.count_key = %(count_key)s AND c.version = %(version)s;
        '''
        return sql
        
countsDAO = CountsDAO()