# -*- coding:utf-8 -*-
'''
Created on Jan 19, 2015

@author: zhuhua
'''
import time
from datetime import datetime
from simpletor.torndb import torndb, Row

class Category(Row):
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
    def find(self, category_id):
        sql = '''
        SELECT * FROM category c WHERE c.id = %s;
        '''
        return torndb.query(sql, category_id)
    
    def all(self):
        sql = '''
        SELECT * FROM category;
        '''
        return torndb.query(sql)
    
categoryDAO = CategoryDAO()
    
class Tag(Row):
    '''
    sample tag 标签（圣诞节，日韩，纯色，新娘，法式，创意，彩绘，糖果）
    '''
    def __init__(self):
        self.id = None
        self.name = None
        self.valid = True

class TagDAO():
    def save(self, tag):
        sql = '''
        INSERT INTO tag(name)  VALUES (%(name)s)
        '''
        torndb.execute(sql, **tag)
    
    def delete(self, tag_id):
        sql = '''
        UPDATE tag SET is_valid = %s
        '''
        torndb.execute(sql, False)
    
tagDAO = TagDAO()
 
class Sample(Row):
    '''
    美甲师作品
    '''
    def __init__(self):
        self.id = None
        self.name = ''
        self.price = 0.0
        self.tag_price = 0.0
        self.sale = 0.0
        self.brief = ''
        self.category_id = None
        self.artisan_id = None
        self.status = 0
        self.tags = ''
        self.create_time = datetime.now()
        self.version = time.time() * 1000
        
class SampleDAO:
    '''
    美甲师作品数据访问接口
    '''
    def save(self, sample):
        sql = '''
        INSERT INTO sample (name, price, tag_price, sale, brief, category_id, artisan_id, status, tags, create_time, version) 
        VALUES (%(name)s, %(price)s, %(tag_price)s, %(sale)s, %(brief)s, %(category_id)s, %(artisan_id)s, %(status)s, %(tags)s, %(create_time)s, %(version)s);
        '''
        return torndb.execute(sql, **sample)
        
    def update(self, sample):
        sql = '''
        UPDATE sample s
        SET name = %(name)s, price = %(price)s, tag_price = %(tag_price)s, sale = %(sale)s, brief = %(brief)s, category_id = %(category_id)s, status = %(status)s, tags = %(tags)s 
        WHERE s.id = %(id)s AND s.version = %(version)s);
        '''
        torndb.execute(sql, **sample)
        
    