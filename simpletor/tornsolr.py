# -*- coding:utf-8 -*-
'''
Created on Jan 23, 2015

@author: zhuhua
'''
import pysolr
import copy
import settings

class index:
    '''save index to solr'''
    def __init__(self, core=''):
        self.core = core
        
    def __call__(self, method):
        def wrapper(*args, **kwds):
            obj = method(*args, **kwds)
            obj_copy = copy.deepcopy(obj)
            
            if isinstance(obj_copy, dict):
                keys = obj_copy.keys()
                for k in keys:
                    v = obj_copy[k]
                    if isinstance(v, dict):
                        for kk, vv in v.iteritems():
                            obj_copy['%s_%s' % (k, kk)] = vv
                        del obj_copy[k]
                    
            solr = pysolr.Solr('%s/%s' % (settings.solr, self.core), timeout=10)
            solr.add([obj_copy])
            return obj
        return wrapper
    
def connect(core=''):
    return pysolr.Solr('%s/%s' % (settings.solr, core), timeout=10)