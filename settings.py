# -*- coding:utf-8 -*-
'''
Created on 2013-3-26

@author: zhuhua
'''
import os

installed_apps = ['api', 'artisan', 'upload', 'backend', 'sample', 'trade', 'evaluate', 'pay']

template_dir = os.path.join(os.path.dirname(__file__), "templates")
static_dir = os.path.join(os.path.dirname(__file__), "static")
img_dir = os.path.join(os.path.dirname(__file__), "img")


db_host = '127.0.0.1'
db_name = 'nail'
db_user = 'root'
db_password = '123456'

default_pass = '123456'

# solr = 'http://127.0.0.1:8983/solr'
solr = 'http://115.28.134.4:8983/solr'

redis = '127.0.0.1'

sms_sname = ''
sms_spwd = ''
sms_sprdid = ''

port = 8888

appointmentRange = (10, 21) #预约时间范围
order_expire_time = 30 # minute
