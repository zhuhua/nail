# -*- coding:utf-8 -*-
'''
Created on Jan 19, 2015

@author: zhuhua
'''
from datetime import datetime
from simpletor import torndb

class Category(torndb.Row):
    '''
    作品类别
    '''
    def __init__(self):
        self.id = None
        self.name = None
        self.create_time = datetime.now()
        
class CategoryDAO:
    '''
    作品类别数据访问接口
    '''
    @torndb.get
    def find(self, category_id):
        sql = '''
        SELECT * FROM category c WHERE c.id = %s;
        '''
        return sql
    
    @torndb.select
    def all(self):
        sql = '''
        SELECT * FROM category;
        '''
        return sql
    
categoryDAO = CategoryDAO()

class Sample(torndb.Row):
    '''
    美甲师作品
    '''
    def __init__(self):
        self.id = None
        self.name = ''
        self.price = 0.0
        self.tag_price = 0.0
        self.sale = 0
        self.brief = ''
        self.category_id = None
        self.artisan_id = None
        self.status = 0
        self.tags = ''
        self.create_time = datetime.now()
        
class SampleDAO:
    '''
    美甲师作品数据访问接口
    '''
    @torndb.insert
    def save(self, **sample):
        sql = '''
        INSERT INTO sample (name, price, tag_price, sale, brief, category_id, artisan_id, status, tags, create_time) 
        VALUES (%(name)s, %(price)s, %(tag_price)s, %(sale)s, %(brief)s, %(category_id)s, %(artisan_id)s, %(status)s, %(tags)s, %(create_time)s);
        '''
        return sql
    
    @torndb.get
    def find(self, sample_id):
        sql = '''
        SELECT * FROM sample s WHERE s.id = %s;
        '''
        return sql
        
    @torndb.update
    def update(self, **sample):
        sql = '''
        UPDATE sample s
        SET name = %(name)s, price = %(price)s, tag_price = %(tag_price)s, sale = %(sale)s, brief = %(brief)s, category_id = %(category_id)s, status = %(status)s, tags = %(tags)s 
        WHERE s.id = %(id)s AND s.version = %(version)s);
        '''
        return sql
        
sampleDAO = SampleDAO()
