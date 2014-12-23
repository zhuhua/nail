# -*- coding:utf-8 -*-
'''
Created on 2014-12-23

@author: zhuhua
'''
from uuid import uuid4
from datetime import datetime
from simpletor.torndb import torndb, Transactional, Row

@Transactional()
def register(mobile, password):
    '''User Register'''
    account = torndb.get('SELECT * FROM account WHERE mobile=%s', mobile)
    if account is not None:
        raise Exception('手机号%s已存在' % mobile)
    
    sql = '''
    INSERT INTO account(id, mobile, password, nick, avatar, reg_time, last_login) 
    VALUES (%(id)s, %(mobile)s, %(password)s, %(nick)s, %(avatar)s, %(reg_time)s, %(last_login)s)
    '''
    now = datetime.now()
    account = Row(id=uuid4().hex, mobile=mobile, password=password, nick='', avatar='', reg_time=now, last_login=now)
    torndb.execute(sql, **account)
    
    return True