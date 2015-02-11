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
        self.create_time = datetime.now()
        self.last_login = datetime.now()
    
class ArtisanDAO:
    '''
    Artist DAO
    '''
    @torndb.insert
    def save(self, artisan):
        sql = '''
        INSERT INTO artisan (name, password, gender, mobile, serv_area, avatar, level, avg_price, cert_pop, cert_pro, brief, create_time, last_login) 
        VALUES (%(name)s, %(password)s, %(gender)s, %(mobile)s, %(serv_area)s, %(avatar)s, %(level)s, %(avg_price)s, %(cert_pop)s, %(cert_pro)s, %(brief)s, %(create_time)s, %(last_login)s);
        '''
        return sql
    
    @torndb.get
    def find(self, artisan_id):
        sql = '''
        SELECT * FROM artisan a WHERE a.id = %s;
        '''
        return sql
        
    @torndb.update
    def update(self, **artisan):
        sql = '''
        UPDATE artisan a SET 
        name = %(name)s, password = %(password)s, gender = %(gender)s, mobile = %(mobile)s, serv_area = %(serv_area)s, avatar = %(avatar)s, avg_price = %(avg_price)s, cert_pop = %(cert_pop)s, cert_pro = %(cert_pop)s, brief = %(brief)s, last_login = %(last_login)s, level = %(level)s 
        WHERE a.id = %(id)s 
        '''
        return sql
        
    @torndb.select
    def all(self):
        sql = '''
        SELECT * FROM artisan;
        '''
        return sql
        
artisanDAO = ArtisanDAO()