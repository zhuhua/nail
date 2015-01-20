# -*- coding:utf-8 -*-
'''
Created on Jan 14, 2015

@author: lisong
'''
from simpletor import application

from sample import services as sample_service

@application.RequestMapping("/api/sample/category/list")
class categorys(application.RequestHandler):
    
    def get(self):
        categorys = sample_service.categorys()
        self.render_json(categorys)

@application.RequestMapping("/api/sample/category")
class category(application.RequestHandler):
    
    def get(self):
        category_id = self.get_argument('category_id', strip=True)
        category = sample_service.category(category_id)
        self.render_json(category)