# -*- coding:utf-8 -*-
'''
Created on Jan 15, 2015

@author: zhuhua
'''
import models

from datetime import datetime
from simpletor.application import AppError
from simpletor.utils import sha1pass
from simpletor.torndb import Transactional

@Transactional()
def login(username, password):
    '''
    登录
    '''
    manager = models.managerDAO.findByName(username)
    if manager is None:
        raise AppError('用户名错误')
    
    if manager.password != sha1pass(password):
        raise AppError('密码错误')
    
    manager.last_lgoin = datetime.now()
    models.managerDAO.update(manager)
    return manager