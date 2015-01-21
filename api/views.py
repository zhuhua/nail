# -*- coding:utf-8 -*-
'''
Created on 2014年12月18日

@author: zhuhua
'''
from simpletor import application
from simpletor.torndb import torndb, transactional

from user import services

@application.RequestMapping("/api/login")
class Login(application.RequestHandler):
    
    @transactional
    def get(self):
        mobile = self.get_argument('mobile', strip=True)
        password = self.get_argument('password', strip=True)
        account = torndb.get('SELECT * FROM account WHERE mobile=%s', mobile)
        self.render_json(account)
        
@application.RequestMapping("/register")
class Register(application.RequestHandler):
    
    def post(self):
        mobile = self.get_argument('mobile', strip=True)
        password = self.get_argument('password', strip=True)
        services.register(mobile, password)
        
# @application.RequestMapping("/account")
# class AccountHandler(application.RequestHandler):
#     
#     def get(self, *args, **kwargs):
#         pass
#     
#     def post(self, *args, **kwargs):
#         pass