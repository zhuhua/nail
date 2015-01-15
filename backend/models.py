# -*- coding:utf-8 -*-
'''
Created on Jan 15, 2015

@author: zhuhua
'''
from simpletor.torndb import torndb, Row

class Manager(Row):
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
    def find(self, manager_id):
        sql = '''
        SELECT * FROM manager m WHERE m.id = %s
        '''
        return torndb.get(sql, manager_id)
    
    def findByName(self, name):
        sql = '''
        SELECT * FROM manager m WHERE m.name = %s
        '''
        return torndb.get(sql, name)
    
    def update(self, manager):
        sql = '''
        UPDATE manager m SET m.password = %(password)s, m.last_login = %(last_login)s WHERE m.id = %(id)s
        '''
        return torndb.execute(sql, **manager)
    
managerDAO = ManagerDAO()