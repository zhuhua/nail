# -*- coding:utf-8 -*-
'''
Created on 2014-12-24

@author: zhuhua
'''
from simpletor import application

from artisan import services as artisan_service

import settings

@application.RequestMapping("/artisan")
class Add(application.RequestHandler):
    
    @application.Security('ROLE_ADMIN', 'ROLE_MANAGER')
    def get(self):
        self.render('artisan/add.html')
        
    @application.Security('ROLE_ADMIN')
    def post(self):
        name = self.get_argument('name', strip=True)
        mobile = self.get_argument('mobile', strip=True)
        password = settings.default_pass
        gender = self.get_argument('gender', default=0, strip=True)
        brief = self.get_argument('brief', default='', strip=True)
        
        artisan_service.register(name, mobile, password, gender=gender, brief=brief)
        self.redirect('/artisans')
                
@application.RequestMapping("/artisans")
class Paging(application.RequestHandler):
    
    def get(self):
        items = artisan_service.search_artisan()
        self.render('artisan/list.html', items=items)
        
        
@application.RequestMapping("/artisan/([0-9]+)")
class Profile(application.RequestHandler):
    
    @application.Security('ROLE_ARTISAN')
    def get(self, artisan_id):
        artisan = artisan_service.get_artisan(artisan_id)
        self.render('artisan/profile.html', item=artisan)
        
@application.RequestMapping("/artisan/([0-9]+)/profile")
class Edit(application.RequestHandler):
    
    @application.Security('ROLE_ARTISAN')
    def get(self, artisan_id):
        artisan = artisan_service.get_artisan(artisan_id)
        self.render('artisan/edit.html', item=artisan)
        
    @application.Security('ROLE_ARTISAN')
    def post(self, artisan_id):
        name = self.get_argument('name', strip=True)
        mobile = self.get_argument('mobile', strip=True)
        gender = self.get_argument('gender', default=0, strip=True)
        brief = self.get_argument('brief', default='', strip=True)
        artisan_service.update_profile(artisan_id, name=name, mobile=mobile, gender=gender, brief=brief)
        self.redirect('/artisan/%s' % artisan_id)

@application.RequestMapping("/artisan/([0-9]+)/avatar")
class UploadAvatar(application.RequestHandler):
    
    @application.Security('ROLE_ARTISAN')
    def get(self, artisan_id):
        self.render('artisan/avatar.html')
        
    @application.Security('ROLE_ARTISAN')
    def post(self, artisan_id):
        avatar = self.get_argument('avatar', strip=True)
        artisan_service.update_profile(artisan_id, avatar=avatar)
        self.redirect('/artisan/%s' % artisan_id)