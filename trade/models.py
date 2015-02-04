# -*- coding:utf-8 -*-
'''
Created on Jan 28, 2015

@author: lisong
'''
from datetime import datetime
from simpletor import torndb

    
class Order(torndb.Row):
    '''
    订单
    '''
    def __init__(self):
        self.id = None
        self.user_id = None
        self.buyer_name = None
        self.address = None
        self.telephone = None
        self.title = None
        self.order_no = None
        self.trade_no = None
        self.status = 0
        self.create_time = datetime.now()
        self.update_time = datetime.now()
        self.display_buyer = True
        self.display_seller = True
        self.is_reviewed = False
        self.artisan_id = None
        self.artisan_name = None
        self.sample_id = None
        self.sample_name = None
        self.cover = None
        self.tag_price = None
        self.price = None
        self.remark = None
        
class OrderDAO:
    '''
    订单数据访问接口
    '''
    @torndb.get
    def find(self, order_id):
        sql = '''
        SELECT * FROM orders o WHERE o.id = %s;
        '''
        return sql
    
    @torndb.get
    def find_by_order_no(self, order_no):
        sql = '''
        SELECT * FROM orders o WHERE o.order_no = %s;
        '''
        return sql
    
    @torndb.get
    def count_orders_by_seller(self, artisan_id, status = None):
        sql = '''
        SELECT COUNT(id) FROM orders o 
        WHERE o.artisan_id = %s AND o.status = %s AND o.display_seller = true;
        '''
        if status == None:
            sql = '''
            SELECT COUNT(id) FROM orders o 
            WHERE o.artisan_id = %s AND o.display_seller = true;
            '''
        return sql
    
    @torndb.select
    def find_orders_by_seller(self, artisan_id, status = None, max_results = 0, first_result = 10):
        sql = '''
        SELECT * FROM orders o 
        WHERE o.artisan_id = %s AND o.status = %s AND o.display_seller = true 
        LIMIT %s OFFSET %s;
        '''
        if status == None:
            sql = '''
            SELECT * FROM orders o 
            WHERE o.artisan_id = %s AND o.display_seller = true 
            LIMIT %s OFFSET %s;
            '''
            
        return sql
    
    @torndb.get
    def count_orders_by_buyer(self, artisan_id, status = None):
        sql = '''
        SELECT COUNT(id) FROM orders o 
        WHERE o.user_id = %s AND o.status = %s AND o.display_buyer = true;
        '''
        if status == None:
            sql = '''
            SELECT COUNT(id) FROM orders o 
            WHERE o.user_id = %s AND o.display_buyer = true;
            '''
            
        return sql
    
    @torndb.select
    def find_orders_by_buyer(self, user_id, status = None, max_results = 0, first_result = 10):
        sql = '''
        SELECT * FROM orders o 
        WHERE o.user_id = %s AND o.status = %s AND o.display_buyer = true 
        LIMIT %s OFFSET %s;
        '''
        if status == None:
            sql = '''
            SELECT * FROM orders o 
            WHERE o.user_id = %s AND o.display_buyer = true LIMIT %s OFFSET %s;
            '''
        return sql
    
    @torndb.select
    def count_orders_by_admin(self, buyer = None, seller = None, status = None, 
                              start_date = None, end_date = None):
        params = list()
        has_params = False
        if buyer == None:
            params.append('%s')
        else:
            params.append('o.user_id = %s')
            has_params = True
            
        if seller == None:
            params.append('%s')
        else:
            params.append('o.artisan_id = %s')
            has_params = True
        
        if status == None:
            params.append('%s')
        else:
            params.append('o.status = %s')
            has_params = True
            
        if start_date == None:
            params.append('%s')
        else:
            params.append('o.create_time > %s')
            has_params = True
            
        if start_date == None:
            params.append('%s')
        else:
            params.append('o.create_time < %s')
            has_params = True
            
        sql = '''
        SELECT COUNT(id) FROM orders o;
        '''
        if has_params:
            sql = '%s WHERE %s' % (sql, ' '.join(params))
        return sql
    
    @torndb.select
    def find_orders_by_admin(self, buyer = None, seller = None, status = None, 
                              start_date = None, end_date = None, max_results = 0, first_result = 10):
        params = list()
        has_params = False
        if buyer == None:
            params.append('%s')
        else:
            params.append('o.user_id = %s')
            has_params = True
            
        if seller == None:
            params.append('%s')
        else:
            params.append('o.artisan_id = %s')
            has_params = True
        
        if status == None:
            params.append('%s')
        else:
            params.append('o.status = %s')
            has_params = True
            
        if start_date == None:
            params.append('%s')
        else:
            params.append('o.create_time > %s')
            has_params = True
            
        if start_date == None:
            params.append('%s')
        else:
            params.append('o.create_time < %s')
            has_params = True
            
        sql = '''
        SELECT COUNT(id) FROM orders o;
        '''
        if has_params:
            sql = '%s WHERE %s LIMIT %%s OFFSET %%s' % (sql, ' '.join(params))
        return sql
    
    def save(self, **order):
        sql = '''
        INSERT INTO orders (user_id, buyer_name, address, 
        telephone, title, order_no, trade_no, status, create_time, 
        update_time, display_buyer, display_seller, is_reviewed, 
        artisan_id, artisan_name, sample_id, sample_name, cover, 
        tag_price) 
        VALUES ('%(user_id)s', '%(buyer_name)s', '%(address)s', 
        '%(telephone)s', '%(title)s', '%(order_no)s', 
        '%(trade_no)s', '%(status)s', '%(create_time)s', 
        '%(update_time)s', '%(display_buyer)s', '%(display_seller)s', 
        '%(is_reviewed)s', '%(artisan_id)s', '%(artisan_name)s', 
        '%(sample_id)s', '%(sample_name)s', '%(cover)s', '%(tag_price)s', '%(price)s');
        '''
        
        return sql
    
orderDAO = OrderDAO()

class OrderLog(torndb.Row):
    '''
    订单流转日志
    '''
    def __init__(self):
        self.id = None
        self.name = None
        
class OrderLogDAO:
    '''
    订单流转数据访问接口
    '''
    @torndb.select
    def all(self):
        sql = '''
        SELECT * FROM tag;
        '''
        return sql
    
orderLogDAO = OrderLogDAO()

class Appointment(torndb.Row):
    '''
    手艺人预约记录
    '''
    def __init__(self):
        self.id = None
        self.artisan_id = None
        self.sample_id = None
        self.user_id = None
        self.appt_date = None
        self.appt_hour = None
        self.order_no = None
        self.create_time = datetime.now()
        
class AppointmentDAO:
    '''
    订单流转数据访问接口
    '''
    @torndb.select
    def find(self, artisan_id, appt_date):
        sql = '''
        SELECT * FROM appointment WHERE artisan_id = %s and appt_date = %s;
        '''
        return sql
    
    @torndb.insert
    def save(self, **appt):
        sql = '''
        INSERT INTO appointment (artisan_id, sample_id, user_id, 
        appt_date, appt_hour, order_no, create_time) 
        VALUES (%(artisan_id)s, %(sample_id)s, %(user_id)s, 
        %(appt_date)s, %(appt_hour)s, %(order_no)s, %(create_time)s);
        '''
        return sql
    
appointmentDAO = AppointmentDAO()