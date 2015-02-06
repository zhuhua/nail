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
        self.sample_tag_price = None
        self.sample_price = None
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
    def count_orders_by_seller(self, artisan_id):
        sql = '''
        SELECT COUNT(id) FROM orders o 
        WHERE o.artisan_id = %s AND o.display_seller = true;
        '''
        return sql
    
    @torndb.get
    def count_orders_by_seller_status(self, artisan_id, status):
        sql = '''
        SELECT COUNT(id) FROM orders o 
        WHERE o.artisan_id = %s AND o.status = %s AND o.display_seller = true;
        '''
        return sql
    
    @torndb.select
    def find_orders_by_seller(self, artisan_id, max_results = 0, first_result = 10):
        sql = '''
        SELECT * FROM orders o 
        WHERE o.artisan_id = %s AND o.display_seller = true 
        LIMIT %s OFFSET %s;
        '''
        return sql
    
    @torndb.select
    def find_orders_by_seller_status(self, artisan_id, status, max_results = 0, first_result = 10):
        sql = '''
        SELECT * FROM orders o 
        WHERE o.artisan_id = %s AND o.status = %s AND o.display_seller = true 
        LIMIT %s OFFSET %s;
        '''
        return sql
    
    @torndb.get
    def count_orders_by_buyer(self, artisan_id):
        sql = '''
        SELECT COUNT(id) FROM orders o 
        WHERE o.user_id = %s AND o.display_buyer = true;
        '''
            
        return sql
    
    @torndb.get
    def count_orders_by_buyer_status(self, artisan_id, status):
        sql = '''
        SELECT COUNT(id) FROM orders o 
        WHERE o.user_id = %s AND o.status = %s AND o.display_buyer = true;
        '''
        return sql
    
    @torndb.select
    def find_orders_by_buyer(self, user_id, max_results = 0, first_result = 10):
        sql = '''
        SELECT * FROM orders o 
        WHERE o.user_id = %s AND o.display_buyer = true LIMIT %s OFFSET %s;
        '''
        return sql
    
    @torndb.select
    def find_orders_by_buyer_status(self, user_id, status, max_results = 0, first_result = 10):
        sql = '''
        SELECT * FROM orders o 
        WHERE o.user_id = %s AND o.status = %s AND o.display_buyer = true 
        LIMIT %s OFFSET %s;
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
    
    @torndb.insert
    def save(self, **order):
        sql = '''
        INSERT INTO orders (user_id, buyer_name, address, 
        telephone, title, order_no, trade_no, status, create_time, 
        update_time, display_buyer, display_seller, is_reviewed, 
        artisan_id, artisan_name, sample_id, sample_name,sample_tag_price, 
        sample_price, cover, tag_price, price, remark) 
        VALUES (%(user_id)s, %(buyer_name)s, %(address)s, 
        %(telephone)s, %(title)s, %(order_no)s, 
        %(trade_no)s, %(status)s, %(create_time)s, 
        %(update_time)s, %(display_buyer)s, %(display_seller)s, 
        %(is_reviewed)s, %(artisan_id)s, %(artisan_name)s, 
        %(sample_id)s, %(sample_name)s, %(sample_tag_price)s, %(sample_price)s, 
        %(cover)s, %(tag_price)s, %(price)s, %(remark)s);
        '''
        
        return sql
    
    @torndb.update
    def update(self, **order):
        sql = '''
        UPDATE orders SET status = %(status)s, update_time = %(update_time)s, 
        display_buyer = %(display_buyer)s, display_seller = %(display_seller)s, 
        is_reviewed = %(is_reviewed)s, tag_price = %(tag_price)s, price = %(price)s);
        WHERE order_id = %(order_id)s
        '''
        return sql
    
orderDAO = OrderDAO()

class OrderLog(torndb.Row):
    '''
    订单流转日志
    '''
    def __init__(self):
        self.id = None
        self.trader_id = None
        self.trader_type = None
        self.trader_action = None
        self.order_id = None
        self.create_time = datetime.now()
        
class OrderLogDAO:
    '''
    订单流转数据访问接口
    '''
    @torndb.insert
    def save(self, **orderLog):
        sql = '''
        INSERT INTO order_log (trader_id, trader_type, trader_action, 
        order_id, create_time) 
        VALUES (%(trader_id)s, %(trader_type)s, %(trader_action)s, 
        %(order_id)s, %(create_time)s);
        '''
        return sql
    
    @torndb.select
    def find(self, order_id):
        sql = '''
        SELECT * FROM order_log WHERE order_id = %s;
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