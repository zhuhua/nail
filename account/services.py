# -*- coding:utf-8 -*-
'''
Created on 2014-12-23

@author: zhuhua
'''
from uuid import uuid4
from simpletor.torndb import  Transactional

import hashlib
import models

def sha1pass(password):
    '''Password Hash'''
    sha1 = hashlib.sha1()
    sha1.update(password)
    return sha1.hexdigest()

@Transactional()
def register(mobile, password):
    '''User Register'''
    account = models.accountDAO.findByMobile(mobile)
    if account is not None:
        raise Exception('手机号%s已存在' % mobile)

    account = models.Account()
    account.id = uuid4().hex
    account.mobile = mobile
    account.password = sha1pass(password)
    
    models.accountDAO.save(account)
    return account