# -*- coding:utf-8 -*-
'''
Created on 2014-12-24

@author: zhuhua
'''
from simpletor import application

from artisan import services as artisan_service

import settings

@application.RequestMapping("/manage/artisan")
class AddArtisan(application.RequestHandler):
    
    def get(self):
        self.render('artisan/add_artisan.html')
        
    def post(self):
        name = self.get_argument('name', strip=True)
        mobile = self.get_argument('mobile', strip=True)
        password = settings.DEUATLT_PASS
        gender = self.get_argument('gender', default=0, strip=True)
        brief = self.get_argument('brief', default='', strip=True)
        
        artisan_service.register(name, mobile, password, s=gender, brief=brief)
        self.write('finish')
        

@application.RequestMapping("/manage/artisan/([0-9]+)")
class EditArtisan(application.RequestHandler):
    
    def get(self, artisan_id):
        artisan = artisan_service.get(artisan_id)
        self.render('artisan/edit_artisan.html', item=artisan)
        
    def post(self):
        self.render('artisan/edit_artisan.html')
        
        
@application.RequestMapping("/manage/artisans")
class ListArtisan(application.RequestHandler):
    
    def get(self):
        self.render('artisan/artisan.html')
        
    def post(self):
        self.render('artisan/artisan.html')
        
    