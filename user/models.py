# -*- coding:utf-8 -*-
'''
Created on 2014-12-23

@author: zhuhua
'''
from uuid import uuid4
from datetime import datetime
from simpletor import torndb
import time
from sqlite3.dbapi2 import sqlite_version_info

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

class Address(torndb.Row):
    '''常用地址'''
    def __init__(self):
        self.id = None
        self.user_id = None
        self.location = ''
        self.detail = ''
        self.is_default = True
        self.create_time = datetime.now()
        
class AddressDAO:
    '''常用地址数据接口'''
    @torndb.insert
    def save(self, **address):
        sql = '''
        INSERT INTO address(user_id, location, detail, is_default, create_time) 
        VALUES (%(user_id)s, %(location)s, %(detail)s, %(is_default)s, %(create_time)s);
        '''
        return sql
    
    @torndb.get
    def find(self, address_id):
        sql = '''
        SELECT * FROM address a WHERE a.id = %s;
        '''
        return sql
        
    @torndb.select
    def find_by_user(self, user_id):
        sql = '''
        SELECT * FROM address a WHERE a.user_id = %s ORDER BY a.create_time DESC;
        '''
        return sql
    
    @torndb.get
    def find_default(self, user_id):
        sql = '''
        SELECT * FROM address a WHERE a.is_default = 1 AND a.user_id = %s;
        '''
        return sql
    
    @torndb.update
    def change_default(self, is_default, address_id, user_id):
        sql = '''
        UPDATE address a SET a.is_default = %s WHERE a.id = %s AND a.user_id = %s;
        '''
        return sql
    
    @torndb.delete
    def delete(self, address_id):
        sql = '''
        DELETE FROM address WHERE id = %s;
        '''
        return sql
    
addressDAO = AddressDAO()
        
class Favorite(torndb.Row):
    '''收藏'''
    def __init__(self):
        self.id = None
        self.user_id = None
        self.object_id = None
        self.type = None
        self.status = 0
        self.update_time = datetime.now()
        self.create_time = datetime.now()
        
class FavoriteDAO:
    '''收藏数据接口'''
    @torndb.insert
    def save(self, **favorite):
        sql = '''
        INSERT INTO favorite(user_id, object_id, type, status, update_time, create_time) 
        VALUES (%(user_id)s, %(object_id)s, %(type)s, %(status)s, %(update_time)s, %(create_time)s);
        '''
        return sql
        
    @torndb.get
    def find(self, favorite_id, status = 0):
        sql = '''
        SELECT * FROM favorite f WHERE f.id = %s AND f.status = %s;
        '''
        return sql
    
    @torndb.get
    def find_by_object(self, **favorite):
        sql = '''
        SELECT * FROM favorite f 
        WHERE f.user_id = %(user_id)s AND f.type = %(type)s 
            AND f.object_id = %(object_id)s AND f.status = %(status)s;
        '''
        return sql
    
    @torndb.select
    def find_by_user_objects(self, user_id, fav_type, object_ids, status = 0):
        sql = '''
        SELECT * FROM favorite f 
        WHERE f.user_id = %s AND f.type = %s AND f.object_id in %s AND f.status = %s;
        '''
        return sql
    
    @torndb.select
    def find_by_user(self, user_id, fav_type, status = 0, limit=10, offset=0):
        sql = '''
        SELECT * FROM favorite f 
        WHERE f.user_id = %s AND f.type = %s  AND f.status = %s 
        ORDER BY f.update_time DESC LIMIT %s OFFSET %s;
        '''
        return sql
    
    @torndb.update
    def update(self, **favorite):
        sql = '''
        UPDATE favorite f SET f.status = %(status)s, f.update_time = %(update_time)s WHERE f.id = %(id)s
        '''
        
        return sql
    
    @torndb.delete
    def delete(self, favorite_id):
        sql = '''
        DELETE FROM favorite WHERE id = %s;
        '''
        return sql
        
favoriteDAO = FavoriteDAO()