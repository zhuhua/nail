'''
Created on 2013-3-26

@author: zhuhua
'''
import os

installed_apps = ['apstat']

template_dir = os.path.join(os.path.dirname(__file__), "templates")
static_dir = os.path.join(os.path.dirname(__file__), "static")

database_connection_url = 'mysql+mysqldb://%s:%s@localhost:3306/mybatis_demo?charset=utf8' % ('root', '123456')

port = 8888
