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
        
        user, role, avatar = '', '', ''
        home = ''
        
        if re.match('[0-9]*', login_id).group() == '':
            user, role, avatar = self.manager_login(login_id, password)
            home = '/artisans'
        else:
            user, role, avatar = self.artisan_login(login_id, password)
            home = '/artisan/%s' % user.id
            
        current_user = dict(id=user.id, name=user.name, role=role, avatar=avatar)
        self.set_current_user(current_user)
        
        self.redirect(home)
        
    def manager_login(self, username, password):
        manager = manager_serv.login(username, password)
        return manager, manager.role, '/static/image/avatar.png'

    def artisan_login(self, artisan_id, password):
        artisan = artisan_serv.login(artisan_id, password)
        avatar = artisan.avatar
        if avatar is None or avatar == '':
            avatar = '/static/image/avatar.png'
        return artisan, 'ROLE_ARTISAN', avatar
        
@application.RequestMapping("/logout")
class Logout(application.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/login')
        

@application.RequestMapping("/")
class Index(application.RequestHandler):
    
    @application.Security('ROLE_ADMIN', 'ROLE_MANAGER', 'ROLE_ARTISAN')
    def get(self):
        self.render('index.html')