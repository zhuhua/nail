# -*- coding:utf-8 -*-
'''
Created on Jan 14, 2015

@author: lisong
'''
from simpletor.torndb import Transactional

import models

def categorys():
    categorys = models.categoryDAO.all()
    return categorys

def category(category_id):
    return models.categoryDAO.find(category_id)