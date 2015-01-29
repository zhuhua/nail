# -*- coding:utf-8 -*-
'''
Created on 2013-3-26

@author: zhuhua
'''
import os

installed_apps = ['api', 'artisan', 'upload', 'backend', 'sample']

template_dir = os.path.join(os.path.dirname(__file__), "templates")
static_dir = os.path.join(os.path.dirname(__file__), "static")
img_dir = os.path.join(os.path.dirname(__file__), "img")

db_host = '127.0.0.1'
db_name = 'nail'
db_user = 'root'
db_password = '123456'

default_pass = '123456'

solr = 'http://127.0.0.1:8983/solr'
redis = '127.0.0.1'

port = 8888