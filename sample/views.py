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
    
    @application.Security('ROLE_ARTISAN')
    def get(self):
        categories = sample_services.get_categories()
        tags = sample_services.get_tags()
        sample = sample_models.Sample()
        sample.images = []
        self.render('sample/add.html', item=sample, categories=categories, tags=tags)
        
    @application.Security('ROLE_ARTISAN')
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
        
        try:
            sample_services.add_sample(sample)
        except application.AppError, e:
            self.add_error(e)
            categories = sample_services.get_categories()
            tags = sample_services.get_tags()
            self.render('sample/add.html', item=sample, categories=categories, tags=tags)
            return
            
        self.redirect('/samples')
        
@application.RequestMapping("/sample/([0-9]+)")
class Edit(application.RequestHandler):
    
    @application.Security('ROLE_ARTISAN')
    def get(self, sample_id):
        categories = sample_services.get_categories()
        tags = sample_services.get_tags()
        sample = sample_services.get_sample(sample_id)
        self.render('sample/edit.html', item=sample, categories=categories, tags=tags)
        
    @application.Security('ROLE_ARTISAN')
    def post(self, sample_id):
        sample = sample_services.get_sample(sample_id)
        sample.name = self.get_argument('name', strip=True)
        sample.category_id = self.get_argument('category_id', strip=True)
        sample.tag_price = self.get_argument('tag_price', strip=True)
        sample.price = self.get_argument('price', strip=True)
        sample.images = self.get_arguments('image', strip=True)
        sample.brief = self.get_argument('brief', strip=True)
        sample.tags = ' '.join(self.get_arguments('tags', strip=True))
        
        sample_services.update_sample(sample)
        self.redirect('/samples')

@application.RequestMapping("/sample/delete/([0-9]+)")
class Delete(application.RequestHandler):
    
    @application.Security('ROLE_ARTISAN')
    def get(self, sample_id):
        sample = sample_services.get_sample(sample_id)
        sample.status = 1
        sample_services.update_sample(sample)
        self.redirect('/samples')
        
@application.RequestMapping("/samples")
class List(application.RequestHandler):
    
    @application.Security('ROLE_ARTISAN')
    def get(self):
        page = self.get_argument('page', '1', strip=True)
        page_size = 10
        artisan_id = self.get_current_user()['id']
        items, hits = sample_services.search_sample(artisan_id=artisan_id, page=page, page_size=page_size)
        self.render('sample/list.html', items=items, page=page, page_size=page_size, total=hits)
        
@application.RequestMapping("/sample/index/update")
class UpdateIndex(application.RequestHandler):
    
    @application.Security('ROLE_ADMIN')
    def get(self):
        items = sample_models.sampleDAO.all()
        for item in items:
            sample_services.update_sample_index(item.id)
            
        self.finish("update sample index %s" % len(items))