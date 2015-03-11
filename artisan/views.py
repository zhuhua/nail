# -*- coding:utf-8 -*-
'''
Created on 2014-12-24

@author: zhuhua
'''
from simpletor import application

from artisan import models as artisan_models
from artisan import services as artisan_service
from common import services as common_service

import settings

@application.RequestMapping("/artisan")
class Add(application.RequestHandler):
    
    @application.Security('ROLE_ADMIN', 'ROLE_MANAGER')
    def get(self):
        artisan = artisan_models.Artisan()
        self.render('artisan/add.html', item=artisan)
        
    @application.Security('ROLE_ADMIN')
    def post(self):
        artisan = artisan_models.Artisan()
        artisan.name = self.get_argument('name', strip=True)
        artisan.mobile = self.get_argument('mobile', strip=True)
        artisan.password = settings.default_pass
        artisan.gender = self.get_argument('gender', default=0, strip=True)
        artisan.brief = self.get_argument('brief', default='', strip=True)
        
        try:
            artisan_service.register(artisan)
        except application.AppError, e:
            self.add_error(e)
            self.render('artisan/add.html', item=artisan)
            return
            
        self.redirect('/artisans')
                
@application.RequestMapping("/artisans")
class List(application.RequestHandler):
    
    @application.Security('ROLE_ADMIN', 'ROLE_MANAGER')
    def get(self):
        page = self.get_argument('page', '1', strip=True)
        page_size = 10
        items, hits = artisan_service.search_artisan(page=page, page_size=page_size)
        self.render('artisan/list.html', items=items, page=page, page_size=page_size, total=hits)
        
        
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
        artisan = artisan_service.get_artisan(artisan_id)
        artisan.name = self.get_argument('name', strip=True)
        artisan.mobile = self.get_argument('mobile', strip=True)
        artisan.gender = self.get_argument('gender', default=0, strip=True)
        artisan.brief = self.get_argument('brief', default='', strip=True)
        artisan.serv_area = self.get_argument('serv_area', default='', strip=True)
        
        try:
            artisan_service.update_profile(artisan)
        except application.AppError, e:
            self.add_error(e)
            self.render('artisan/edit.html', item=artisan)
            return
            
        self.redirect('/artisan/%s' % artisan_id)

@application.RequestMapping("/gallery")
class UploadToGallery(application.RequestHandler):
    
    @application.Security('ROLE_ARTISAN')
    def get(self):
        artisan_id = self.get_current_user()['id']
        gallery = common_service.get_gallery(artisan_id, 'artisan')
        i, tmp, items = 0, [], []
        for item in gallery:
            tmp.append(item)
            if i % 6 == 5:
                items.append(tmp)
                tmp = []
            i += 1
        items.append(tmp)
        self.render('artisan/gallery.html', items=items)
        
    @application.Security('ROLE_ARTISAN')
    def post(self):
        artisan_id = self.get_current_user()['id']
        url = self.get_argument('url', strip=True)
        common_service.add_to_gallery(artisan_id, 'artisan', url)
        
        artisan = artisan_service.get_artisan(artisan_id)
        artisan.avatar = url
        artisan_service.update_profile(artisan)
        self.redirect('/gallery')
        
@application.RequestMapping("/gallery/([0-9]+)")
class RemoveFromGallery(application.RequestHandler):
    
    @application.Security('ROLE_ARTISAN')
    def get(self, gallery_id):
        common_service.remove_from_gallery(gallery_id)
        self.redirect('/gallery')