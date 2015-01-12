# -*- coding:utf-8 -*-
'''
Created on 2014年12月18日

@author: zhuhua
'''
import json
import hashlib
from datetime import date, datetime

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
        
def sha1pass(password):
    '''Password Hash'''
    sha1 = hashlib.sha1()
    sha1.update(password)
    return sha1.hexdigest()
