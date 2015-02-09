# -*- coding:utf-8 -*-
'''
Created on 2015-02-09

@author: lisong
'''
from datetime import datetime
from simpletor import torndb

class Evaluate(torndb.Row):
    '''
    评价
    '''
    def __init__(self):
        self.id = None
        self.author_id = None
        self.object_id = None
        self.object_type = None
        self.content = None
        self.rating = 0
        self.communication_rank = None
        self.professional_rank = None
        self.punctual_rank = None
        self.create_time = datetime.now()
        self.is_block = False
        self.is_valid = True
        
class EvaluateDAO():
    '''
    评价数据访问接口
    '''
    @torndb.get
    def find(self, evaluate_id):
        sql = '''
        SELECT * FROM evaluate o WHERE o.id = %s;
        '''
        return sql
    
    @torndb.get
    def count_obj_id(self, object_id, object_type):
        sql = '''
        SELECT COUNT(id) AS total FROM evaluate o WHERE o.object_id = %s AND o.object_type = %s;
        '''
        return sql
    
    @torndb.select
    def find_obj_id(self, object_id, object_type, max_results, first_result):
        sql = '''
        SELECT * FROM evaluate o WHERE o.object_id = %s AND o.object_type = %s LIMIT %s OFFSET %s;
        '''
        return sql
    
    @torndb.insert
    def save(self, **evaluate):
        sql = '''
        INSERT INTO evaluate (author_id, object_id, object_type, 
        content, rating, communication_rank, professional_rank,
        punctual_rank, create_time, is_block, is_valid) 
        VALUES (%(author_id)s, %(object_id)s, %(object_type)s, 
        %(content)s,%(rating)s, %(communication_rank)s, %(professional_rank)s, 
        %(punctual_rank)s, %(create_time)s, %(is_block)s, %(is_valid)s); 
        '''
        return sql
    
    @torndb.update
    def update(self, **evaluate):
        sql = '''
        UPDATE evaluate SET is_block = %(is_block)s, is_valid = %s(is_valid)% WHERE id = %(id)s
        '''
        return sql
    
evaluateDAO = EvaluateDAO()