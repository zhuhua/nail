# -*- coding:utf-8 -*-
'''
Created on 2014-12-24

@author: zhuhua
'''
from simpletor import application

from artisan import services as artisan_service

import settings

@application.RequestMapping("/manage/artisan")
class Add(application.RequestHandler):
    
    def get(self):
        self.render('artisan/add.html')
        
    def post(self):
        name = self.get_argument('name', strip=True)
        mobile = self.get_argument('mobile', strip=True)
        password = settings.default_pass
        gender = self.get_argument('gender', default=0, strip=True)
        brief = self.get_argument('brief', default='', strip=True)
        
        artisan_service.register(name, mobile, password, s=gender, brief=brief)
        self.redirect('/manage/artisans')
        

@application.RequestMapping("/manage/artisan/([0-9]+)")
class Edit(application.RequestHandler):
    
    def get(self, artisan_id):
        artisan = artisan_service.get(artisan_id)
        self.render('artisan/edit.html', item=artisan)
        
    def post(self):
        self.render('artisan/edit.html')
        
        
@application.RequestMapping("/manage/artisans")
class Paging(application.RequestHandler):
    
    def get(self):
        items = artisan_service.paging(1, 10)
        self.render('artisan/list.html', items=items)
        

@application.RequestMapping("/manage/artisan/([0-9]+)/avatar")
class UploadAvatar(application.RequestHandler):
    
    def get(self, artisan_id):
        self.render('artisan/avatar.html')
        
    def post(self, artisan_id):
        avatar = self.get_argument('avatar', strip=True)
        artisan_service.update_profile(artisan_id, avatar=avatar)
        self.redirect('/manage/artisan/%s' % artisan_id)