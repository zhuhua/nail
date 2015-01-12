# -*- coding:utf-8 -*-
'''
Created on 2013-3-26

@author: zhuhua
'''
import os

installed_apps = ['api', 'backend']

template_dir = os.path.join(os.path.dirname(__file__), "templates")
static_dir = os.path.join(os.path.dirname(__file__), "static")

db_host='127.0.0.1'
db_name='nail'
db_user='root'
db_password='123456'

DEUATLT_PASS = '123456'

port = 8888
