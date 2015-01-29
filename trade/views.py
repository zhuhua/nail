# -*- coding:utf-8 -*-
'''
Created on Jan 28, 2015

@author: lisong
'''
import datetime
from simpletor import application
from trade import services as trade_services

@application.RequestMapping("/appointment/status")
class Add(application.RequestHandler):
    
    def get(self):
        artisan_id = self.get_argument('artisan_id', strip=True)
        appt_date = self.get_argument('appt_date', strip=True)
        tmp_date = appt_date.split("-")
        appt_date = datetime.date(int(tmp_date[0]), int(tmp_date[1]), int(tmp_date[2]))
        apptss = trade_services.appointment_status(artisan_id, appt_date);
        self.render_json(apptss)

'''
@application.RequestMapping("/sample/([0-9]+)")
class Edit(application.RequestHandler):
    
    def get(self, sample_id):
        categories = sample_services.get_categories()
        tags = sample_services.get_tags()
        sample = sample_services.get_sample(sample_id)
        self.render('sample/edit.html', item=sample, categories=categories, tags=tags)
        
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
        
@application.RequestMapping("/samples")
class List(application.RequestHandler):
    def get(self):
        artisan_id = self.get_current_user()['id']
        items, hits = sample_services.search_sample(artisan_id)
        self.render('sample/list.html', items=items)
        '''