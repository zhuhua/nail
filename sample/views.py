# -*- coding:utf-8 -*-
'''
Created on Jan 20, 2015

@author: zhuhua
'''
from simpletor import application
from sample import models as sample_models
from sample import services as sample_services

import settings

@application.RequestMapping("/sample")
class Add(application.RequestHandler):
    
    def get(self):
        categories = sample_services.get_categories()
        self.render('sample/add.html', categories=categories)
        
    def post(self):
        sample = sample_models.Sample()
        sample.name = self.get_argument('name', strip=True)
        sample.artisan_id = self.get_current_user()['id']
        sample.category_id = self.get_argument('category_id', strip=True)
        sample.tag_price = self.get_argument('tag_price', strip=True)
        sample.price = self.get_argument('price', strip=True)
        sample.images = self.get_arguments('image', strip=True)
        sample.brief = self.get_argument('brief', strip=True)
        sample.tags = self.get_argument('tags', strip=True)
        
        sample_services.add_sample(sample)
        self.redirect('/samples')
        
        