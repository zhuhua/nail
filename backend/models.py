# -*- coding:utf-8 -*-
'''
Created on Jan 15, 2015

@author: zhuhua
'''
from simpletor import torndb

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
    def find(self, **kwds):
        sql = '''
        SELECT * FROM manager m WHERE m.id = %s
        '''
        return sql
    
    def findByName(self, **kwds):
        sql = '''
        SELECT * FROM manager m WHERE m.name = %(name)s
        '''
        return sql
    
    def update(self, **kwds):
        sql = '''
        UPDATE manager m SET m.password = %(password)s, m.last_login = %(last_login)s WHERE m.id = %(id)s
        '''
        return sql
    
managerDAO = ManagerDAO()