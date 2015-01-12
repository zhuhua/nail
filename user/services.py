# -*- coding:utf-8 -*-
'''
Created on 2014-12-23

@author: zhuhua
'''
from uuid import uuid4
from datetime import datetime
from simpletor.torndb import Transactional
from simpletor.application import AppError
from simpletor.utils import sha1pass

import time
import models

@Transactional()
def register(mobile, password):
    '''User Register'''
    user = models.userDAO.findByMobile(mobile)
    if user is not None:
        raise AppError('手机号%s已存在' % mobile)

    user = models.User()
    user.mobile = mobile
    user.password = sha1pass(password)
    
    models.userDAO.save(user)
    return user

@Transactional()
def login(mobile, password):
    '''Login'''
    user = models.userDAO.findByMobile(mobile)
    if user is None:
        raise AppError('手机号不存在')
    
    if user.password != sha1pass(password):
        raise AppError('密码错误')
    
    user_id = user.id
    token = models.loginTokenDAO.findByUser(user_id)
    
    if token is None:
        token = models.LoginToken()
        token.user_id = user_id
        models.loginTokenDAO.save(token)
    else:
        token.token = uuid4().hex
        token.expire = time.time() + 86400 * 30
        token.last_login = datetime.now()
        models.loginTokenDAO.update(token)
        
    return token