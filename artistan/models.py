# -*- coding:utf-8 -*-
'''
Created on 2015-1-11

@author: Zhuhua
'''
from datetime import datetime
from simpletor.torndb import torndb, Row

class Artist(Row):
    '''
    Artist
    '''
    def __init__(self):
        self.id = None
        self.name = None
        self.password = None
        self.gender = 1
        self.avatar = ''
        self.level = 1
        self.avg_price = 0
        self.cert_pop = False
        self.cert_pro = False
        self.brief = ''
        self.create_time = datetime.now()
    
class ArtistDAO:
    '''
    Artist DAO
    '''
    def save(self, artist):
        sql = '''
        INSERT INTO artistan (name, password, gender, avatar, level, avg_price, cert_pop, cert_pro, brief, create_time) 
        VALUES (%(name)s, %(password)s, %(gender)s, %(avatar)s, %(level)s, %(avg_price)s, %(cert_pop)s, %(cert_pro)s, %(brief)s, %(create_time)s);
        '''
        torndb.execute(sql, **artist)
        return artist
    
    def find(self, artist_id):
        sql = '''
        SELECT * FROM artistan a WHERE a.id = %s;
        '''
        return torndb.get(sql, artist_id)
        
    def update(self, artist):
        sql = '''
        UPDATE artistan a SET 
        name = %(name)s, password = %(password)s, gender = %(gender)s, avatar = %(avatar)s, avg_price = %(avg_price)s, cert_pop = %(cert_pop)s, cert_pro = %(cert_pop)s, brief = %(brief)s 
        WHERE a.id = %(id)s 
        '''
        torndb.execute(sql, **artist)
        
artistDAO = ArtistDAO()