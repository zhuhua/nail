# -*- coding:utf-8 -*-
'''
Created on Jan 23, 2015

@author: zhuhua
'''
import pysolr
import settings

class index:
    '''save index to solr'''
    def __init__(self, core=''):
        self.core = core
        
    def __call__(self, method):
        def wrapper(*args, **kwds):
            obj = method(*args, **kwds)
            solr = pysolr.Solr('%s/%s' % (settings.solr, self.core), timeout=10)
            solr.add([obj])
            return obj
        return wrapper
    
def connect(core=''):
    return pysolr.Solr('%s/%s' % (settings.solr, core), timeout=10)