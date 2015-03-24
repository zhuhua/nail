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
        self.image = None
        self.url = None

class BannerDAO:
    '''
    Banner DAO
    '''
    @torndb.select
    def find_all(self):
        sql = '''
        SELECT * FROM banner m
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