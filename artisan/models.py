# -*- coding:utf-8 -*-
'''
Created on 2015-1-11

@author: Zhuhua
'''
from datetime import datetime
from simpletor import torndb

class Artisan(torndb.Row):
    '''
    Artist
    '''
    def __init__(self):
        self.id = None
        self.name = None
        self.password = None
        self.gender = 1
        self.mobile = None
        self.serv_area = ''
        self.avatar = ''
        self.level = 0
        self.avg_price = 0
        self.cert_pop = False
        self.cert_pro = False
        self.brief = ''
        self.status = 0
        self.create_time = datetime.now()
        self.last_login = datetime.now()
    
class ArtisanDAO:
    '''
    Artist DAO
    '''
    @torndb.insert
    def save(self, **artisan):
        sql = '''
        INSERT INTO artisan (name, password, gender, mobile, serv_area, avatar, level, avg_price, cert_pop, cert_pro, brief, status, create_time, last_login) 
        VALUES (%(name)s, %(password)s, %(gender)s, %(mobile)s, %(serv_area)s, %(avatar)s, %(level)s, %(avg_price)s, %(cert_pop)s, %(cert_pro)s, %(brief)s, %(status)s, %(create_time)s, %(last_login)s);
        '''
        return sql
    
    @torndb.get
    def find(self, artisan_id):
        sql = '''
        SELECT * FROM artisan a WHERE a.id = %s AND a.status = 0;
        '''
        return sql
        
    @torndb.update
    def update(self, **artisan):
        sql = '''
        UPDATE artisan a SET 
        name = %(name)s, password = %(password)s, gender = %(gender)s, mobile = %(mobile)s, serv_area = %(serv_area)s, avatar = %(avatar)s, avg_price = %(avg_price)s, cert_pop = %(cert_pop)s, cert_pro = %(cert_pop)s, brief = %(brief)s, last_login = %(last_login)s, level = %(level)s, status = %(status)s 
        WHERE a.id = %(id)s 
        '''
        return sql
    
    @torndb.update
    def change_pass(self, **artisan):
        sql = '''
        UPDATE artisan a SET 
        password = %(password)s
        WHERE a.id = %(id)s 
        '''
        return sql
        
    @torndb.select
    def all(self):
        sql = '''
        SELECT * FROM artisan WHERE status = 0;
        '''
        return sql
    
    @torndb.get
    def count_by_user(self, user_id):
        sql = '''
        SELECT COUNT(DISTINCT a.id) as total FROM artisan a, orders o 
        WHERE a.id = o.artisan_id AND o.status = 4 AND o.user_id = %s AND a.status = 0
        '''
        return sql
        
    @torndb.select
    def find_by_user(self, user_id, order_by, sort, max_results, first_result):
        sql = '''SELECT DISTINCT a.id FROM artisan a, orders o 
                    WHERE a.id = o.artisan_id AND o.status = 4 AND o.user_id = %s AND a.status = 0
                    ORDER BY %s %s LIMIT %s OFFSET %s'''
        
        return sql
    
artisanDAO = ArtisanDAO()