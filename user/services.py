# -*- coding:utf-8 -*-
'''
Created on 2014-12-23

@author: zhuhua
'''
from uuid import uuid4
from datetime import datetime
from simpletor.torndb import transactional
from simpletor.application import AppError
from simpletor.utils import sha1

import time
import models

@transactional
def register(mobile, password):
    '''User Register'''
    user = models.userDAO.findByMobile(mobile)
    if user is not None:
        raise AppError('手机号%s已存在' % mobile)

    user = models.User()
    user.mobile = mobile
    user.password = sha1(password)
    
    models.userDAO.save(user)
    return user

@transactional
def login(mobile, password):
    '''Login'''
    user = models.userDAO.findByMobile(mobile)
    if user is None:
        raise AppError('手机号不存在')
    
    if user.password != sha1(password):
        raise AppError('密码错误')
    
    user_id = user.id
    token = models.loginTokenDAO.findByUser(user_id)
    
    if token is None:
        token = models.LoginToken()
        token.user_id = user_id
        models.loginTokenDAO.save(**token)
    else:
        token.token = uuid4().hex
        token.expire = time.time() + 86400 * 30
        token.last_login = datetime.now()
        models.loginTokenDAO.update(**token)
        
    return token

def get_token(token):
    return models.loginTokenDAO.find(token)

def get_profile(user_id):
    user = models.userDAO.find(user_id)
    return user