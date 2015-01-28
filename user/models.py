# -*- coding:utf-8 -*-
'''
Created on 2014-12-23

@author: zhuhua
'''
from uuid import uuid4
from datetime import datetime
from simpletor import torndb
import time

class User(torndb.Row):
    '''
    User Account
    '''
    def __init__(self):
        self.id = None
        self.mobile = None
        self.password = None
        self.nick = ''
        self.avatar = ''
        self.reg_time = datetime.now()
        
class UserDAO:
    '''
    User Account DAO
    '''
    @torndb.insert
    def save(self, **user):
        sql = '''
        INSERT INTO users(mobile, password, nick, avatar, reg_time) 
        VALUES (%(mobile)s, %(password)s, %(nick)s, %(avatar)s, %(reg_time)s);
        '''
        return sql
    
    @torndb.get
    def find(self, user_id):
        sql = '''
        SELECT * FROM users u WHERE u.id = %s;
        '''
        return sql
    
    @torndb.get
    def findByMobile(self, mobile):
        sql = '''
        SELECT * FROM users u WHERE u.mobile = %s;
        '''
        return sql
        
    @torndb.update
    def update(self, **user):
        sql = '''
        UPDATE users u SET u.password = %(password)s, u.nick = %(nick)s, u.avatar = %(avatar)s
        WHERE u.id = %(id)s;
        '''
        return sql
        
userDAO = UserDAO()

class LoginToken(torndb.Row):
    '''
    Login Token
    '''
    def __init__(self):
        self.id = None
        self.user_id = None
        self.token = uuid4().hex
        self.expire = time.time() + 86400 * 30
        self.last_login = datetime.now()
        
class LoginTokenDAO:
    '''
    LoginToken DAO
    '''
    @torndb.insert
    def save(self, **token):
        sql = '''
        INSERT INTO login_token(user_id, token, expire, last_login) 
        VALUES (%(user_id)s, %(token)s, %(expire)s, %(last_login)s);
        '''
        return sql
        
    @torndb.get
    def find(self, token):
        sql = '''
        SELECT * FROM login_token l WHERE l.token = %s;
        '''
        return sql
        
    @torndb.get
    def findByUser(self, user_id):
        sql = '''
        SELECT * FROM login_token l WHERE l.user_id = %s;
        '''
        return sql
        
    @torndb.update
    def update(self, **token):
        sql = '''
        UPDATE login_token t SET token = %(token)s, expire = %(expire)s, last_login = %(last_login)s
        WHERE t.id = %(id)s;
        '''
        return sql
        
loginTokenDAO = LoginTokenDAO()