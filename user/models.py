# -*- coding:utf-8 -*-
'''
Created on 2014-12-23

@author: zhuhua
'''
from uuid import uuid4
from datetime import datetime
from simpletor.torndb import torndb, Row
import time

class User(Row):
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
    def save(self, user):
        sql = '''
        INSERT INTO users(mobile, password, nick, avatar, reg_time) 
        VALUES (%(mobile)s, %(password)s, %(nick)s, %(avatar)s, %(reg_time)s)
        '''
        torndb.execute(sql, **user)
        
    def findByMobile(self, mobile):
        sql = '''
        SELECT * FROM users u WHERE u.mobile = %s
        '''
        return torndb.get(sql, mobile)
        
    def update(self, user):
        sql = '''
        UPDATE users u SET u.password = %(password)s, u.nick = %(nick)s, u.avater = %(avatar)s
        WHERE u.id = %(id)s
        '''
        torndb.execute(sql, **user)
        
userDAO = UserDAO()

class LoginToken(Row):
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
    def save(self, token):
        sql = '''
        INSERT INTO login_token(user_id, token, expire, last_login) 
        VALUES (%(user_id)s, %(token)s, %(expire)s, %(last_login)s)
        '''
        torndb.execute(sql, **token)
        
    def find(self, token):
        sql = '''
        SELECT * FROM login_token l WHERE l.token = %s
        '''
        return torndb.get(sql, token)
        
    def findByUser(self, user_id):
        sql = '''
        SELECT * FROM login_token l WHERE l.user_id = %s
        '''
        return torndb.get(sql, user_id)
        
    def update(self, token):
        sql = '''
        UPDATE login_token t SET t.token = %(token)s, t.expire = %(expire)s, t.last_login = %(last_login)s
        WHERE t.id = %(id)s
        '''
        torndb.execute(sql, **token)
        
loginTokenDAO = LoginTokenDAO()

class Artisan(Row):
    '''
    美甲师
    '''
    def __init__(self):
        self.id = None
        self.name = None
        self.password = None
        self.avg_price = 0
        self.cert_pop = False
        self.cert_pro = False
        self.brief = ''
    