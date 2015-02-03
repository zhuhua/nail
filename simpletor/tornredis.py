# -*- coding:utf-8 -*-
'''
Created on Jan 28, 2015

@author: zhuhua
'''
import redis
import settings
import inspect

connect = redis.Redis(host=settings.redis, port=6379, db=1)
PATTERN = '%s_%s'

class cache:
    '''CACHAE 基类'''
    def __init__(self, key, prefix='CACHE'):
        self.prefix = prefix
        self.key_args = None
        self.is_k_exp = False
        self._arg_dict = dict()
        
        if key.startswith('#'):
            self.key_args = key.replace('#', '').split('.')
            self.is_k_exp = True
        else:
            self.key = key
            
    def __arg_dict__(self):
        _args = inspect.getargspec(self._method)
        _arg_len = len(self._args)
        _arg_names = _args.args[:_arg_len]
        _kwd_names = _args.args[_arg_len:]
        
        for i in range(_arg_len):
            self._arg_dict[_arg_names[i]] = self._args[i]
            
        for i in range(len(_kwd_names)):
            self._arg_dict[_kwd_names[i]] = _args.defaults[i]
            
        for kwd_name in _kwd_names:
            try:
                self._arg_dict[kwd_name] = self._kwds[kwd_name]
            except KeyError:
                pass
            
    def __get_key__(self):
        self.__arg_dict__()
        key = ''
        if self.is_k_exp:
            if len(self.key_args) == 1:
                key = PATTERN % (self.prefix, self._arg_dict[self.key_args[0]])
            else:
                arg_obj = self._arg_dict[self.key_args[0]]
                if isinstance(arg_obj, dict):
                    key = PATTERN % (self.prefix, arg_obj[self.key_args[1]])
                else:
                    key = PATTERN % (self.prefix, getattr(arg_obj, self.key_args[1]))
        else:
            key = PATTERN % (self.prefix, self.key)
            
        return key

class cacheable(cache):
    '''缓存'''
    def __call__(self, method):
        def wrapper(*args, **kwds):
            self._method = method
            self._args = args
            self._kwds = kwds
            key = self.__get_key__()
            
            result = connect.get(key)
            if result:
                return result
            
            result = method(*args, **kwds)
            connect.set(key, result)
            return result
        return wrapper
    
class cacheevict(cache):
    '''清除缓存'''
    def __call__(self, method):
        def wrapper(*args, **kwds):
            self._method = method
            self._args = args
            self._kwds = kwds
            key = self.__get_key__()
            connect.delete(key)
        return wrapper