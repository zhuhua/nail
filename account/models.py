# -*- coding:utf-8 -*-
'''
Created on 2014-12-23

@author: zhuhua
'''
from datetime import datetime
from simpletor.torndb import torndb, Row

class Account(Row):
    '''
    User Account
    '''    
    def __init__(self):
        self.nick = ''
        self.avatar = ''
        now = datetime.now()
        self.reg_time = now
        
class AccountDAO:
    '''
    User Account DAO
    '''
    def save(self, account):
        sql = '''
        INSERT INTO account(id, mobile, password, nick, avatar, reg_time) 
        VALUES (%(id)s, %(mobile)s, %(password)s, %(nick)s, %(avatar)s, %(reg_time)s)
        '''
        torndb.execute(sql, **account)
        
    def findByMobile(self, mobile):
        sql = '''
        SELECT * FROM account WHERE mobile = %s
        '''
        torndb.execute(sql, mobile)
        
    def update(self, account):
        sql = '''
        UPDATE account a SET a.password = %(password)s, a.nick = %(nick)s, a.avater = %(avatar)s
        WHERE id = %(id)s
        '''
        torndb.execute(sql, **account)
        
accountDAO = AccountDAO()

class LoginToken(Row):
    '''
    Login Token
    '''
    pass