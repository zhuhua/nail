# -*- coding:utf-8 -*-
'''
Created on 2014-12-24

@author: zhuhua
'''
from simpletor import application
from artisan import services as artisan_serv

import services as manager_serv
import models as manager_models
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
            try:
                user, role, avatar = self.manager_login(login_id, password)
                home = '/artisans'
            except application.AppError, e:
                self.add_error(e)
                self.render('login.html')
                return
        else:
            try:
                user, role, avatar = self.artisan_login(login_id, password)
                home = '/artisan/%s' % user.id
            except application.AppError, e:
                self.add_error(e)
                self.render('login.html')
                return
            
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
        
@application.RequestMapping("/banners")
class BannerList(application.RequestHandler):
    
    @application.Security('ROLE_ADMIN', 'ROLE_MANAGER')
    def get(self):
        items = manager_serv.get_banners()
        self.render('backend/banners.html', items=items)
        
@application.RequestMapping("/banner/([0-9]+)")
class Banner(application.RequestHandler):
    
    @application.Security('ROLE_ADMIN', 'ROLE_MANAGER')
    def get(self, banner_id):
        banner = manager_serv.get_banner(banner_id)
        self.render('backend/banner.html', item=banner)
        
    @application.Security('ROLE_ADMIN', 'ROLE_MANAGER')
    def post(self, banner_id):
        banner = manager_models.Banner()
        banner.name = self.get_argument('name', strip=True)
        banner.cover = self.get_argument('image', default= '', strip=True)
        banner.url = self.get_argument('url', strip=True)
        banner.id = self.get_argument('id', strip=True)
        detail = list()
        da = dict()
        da['image'] = self.get_argument('image1', default= '', strip=True)
        da['description'] = self.get_argument('description1', strip=True)
        da['serial_number'] = 0
        detail.append(da)
        db = dict()
        db['image'] = self.get_argument('image2', default= '', strip=True)
        db['description'] = self.get_argument('description2', strip=True)
        db['serial_number'] = 1
        detail.append(db)
       
        banner.detail = detail
        try:
            banner = manager_serv.edit_banner(banner)
        except application.AppError, e:
            self.add_error(e)
            self.render('backend/banner.html', item=banner)
            return
        self.redirect('/banners')