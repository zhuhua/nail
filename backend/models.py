# -*- coding:utf-8 -*-
'''
Created on Jan 15, 2015

@author: zhuhua
'''
from simpletor import torndb


class Banner(torndb.Row):
    '''
    Banner
    '''
    def __init__(self):
        self.id = None
        self.name = None
        self.cover = None
        self.detail = None
        self.serial_number = None
        self.url = None
        

class BannerDAO:
    '''
    Banner DAO
    '''
    @torndb.get
    def find(self, banner_id):
        sql = '''
        SELECT * FROM banner WHERE id = %s
        '''
        return sql
        
    @torndb.select
    def find_all(self):
        sql = '''
        SELECT * FROM banner LIMIT 5 OFFSET 0
        '''
        return sql
    
    @torndb.insert
    def save(self, **banner):
        sql = '''
        INSERT INTO banner (name, cover, detail, serial_number, url) 
        VALUES (%(name)s, %(cover)s, %(detail)s, %(serial_number)s, %(url)s)
        '''
        return sql
    
    @torndb.update
    def update(self, **banner):
        sql = '''
        UPDATE banner SET  name = %(name)s, cover = %(cover)s, detail = %(detail)s,
        serial_number = %(serial_number)s, url = %(url)s
        WHERE id = %(id)s
        '''
        return sql
        
bannerDAO = BannerDAO()

class Manager(torndb.Row):
    '''
    Manager
    '''
    def __init__(self):
        self.id = None
        self.name = None
        self.password = None
        self.role = None
        
class ManagerDAO:
    '''
    Manager DAO
    '''
    @torndb.get
    def find(self, manager_id):
        sql = '''
        SELECT * FROM manager m WHERE m.id = %s
        '''
        return sql
    
    @torndb.get
    def findByName(self, name):
        sql = '''
        SELECT * FROM manager m WHERE m.name = %s
        '''
        return sql
    
    @torndb.update
    def update(self, **manager):
        sql = '''
        UPDATE manager m SET m.password = %(password)s, m.last_login = %(last_login)s WHERE m.id = %(id)s
        '''
        return sql
    
managerDAO = ManagerDAO()