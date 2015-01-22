# -*- coding:utf-8 -*-
'''
Created on Jan 20, 2015

@author: zhuhua
'''
from simpletor import application
from sample import models as sample_models
from sample import services as sample_services

@application.RequestMapping("/sample")
class Add(application.RequestHandler):
    
    def get(self):
        categories = sample_services.get_categories()
        tags = sample_services.get_tags()
        self.render('sample/add.html', categories=categories, tags=tags)
        
    def post(self):
        sample = sample_models.Sample()
        sample.name = self.get_argument('name', strip=True)
        sample.artisan_id = self.get_current_user()['id']
        sample.category_id = self.get_argument('category_id', strip=True)
        sample.tag_price = self.get_argument('tag_price', strip=True)
        sample.price = self.get_argument('price', strip=True)
        sample.images = self.get_arguments('image', strip=True)
        sample.brief = self.get_argument('brief', strip=True)
        sample.tags = ' '.join(self.get_arguments('tags', strip=True))
        
        sample_services.add_sample(sample)
        self.redirect('/samples')
        
@application.RequestMapping("/sample/([0-9]+)")
class Edit(application.RequestHandler):
    
    def get(self, sample_id):
        categories = sample_services.get_categories()
        tags = sample_services.get_tags()
        self.render('sample/add.html', categories=categories, tags=tags)
        
    def post(self, sample_id):
        sample = sample_models.Sample()
        sample.name = self.get_argument('name', strip=True)
        sample.category_id = self.get_argument('category_id', strip=True)
        sample.tag_price = self.get_argument('tag_price', strip=True)
        sample.price = self.get_argument('price', strip=True)
        sample.images = self.get_arguments('image', strip=True)
        sample.brief = self.get_argument('brief', strip=True)
        sample.tags = ' '.join(self.get_arguments('tags', strip=True))
        
        sample_services.add_sample(sample)
        self.redirect('/samples')
