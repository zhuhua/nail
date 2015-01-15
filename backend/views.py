# -*- coding:utf-8 -*-
'''
Created on 2014-12-24

@author: zhuhua
'''
from simpletor import application
from artisan import services as artisan_serv

import services as manager_serv
import re

@application.RequestMapping("/login")
class Login(application.RequestHandler):
    
    def get(self):
        self.render('login.html')
        
    def post(self):
        login_id = self.get_argument('username', strip=True)
        password = self.get_argument('password', strip=True)
        
        user, role = '', ''
        home = ''
        
        if re.match('[0-9]*', login_id).group() == '':
            user, role = self.manager_login(login_id, password)
            home = '/manager'
        else:
            user, role = self.artisan_login(login_id, password)
            home = '/artisan/%s' % user.id

        self.set_secure_cookie('id', str(user.id))
        self.set_secure_cookie('name', user.name)
        self.set_secure_cookie('role', role)
        
        self.redirect(home)
        
    def manager_login(self, username, password):
        manager = manager_serv.login(username, password)
        return manager, manager.role

    def artisan_login(self, artisan_id, password):
        artisan = artisan_serv.login(artisan_id, password)
        return artisan, 'ROLE_ARTISAN'
        
@application.RequestMapping("/logout")
class Logout(application.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        
    def post(self):
        self.get()