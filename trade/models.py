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
        self.buyer_avatar = None
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
        self.artisan_avatar = None
        self.sample_id = None
        self.sample_name = None
        self.sample_tag_price = None
        self.sample_price = None
        self.sample_brief = None
        self.cover = None
        self.tag_price = None
        self.price = None
        self.remark = None
        
class OrderDAO:
    '''
    订单数据访问接口
    '''
    @torndb.get
    def count_expire(self, expire_time):
        sql = '''SELECT COUNT(id) AS total FROM orders o WHERE o.status = 0 AND o.create_time < %s'''
        return sql
    
    @torndb.select
    def find_expire(self, expire_time):
        sql = '''SELECT id, order_no FROM orders o WHERE o.status = 0 AND o.create_time < %s'''
        return sql
    
    @torndb.update
    def execute_expire(self, status, orders_ids):
        sql = '''UPDATE orders SET status = %s WHERE id IN %s'''
        return sql
    
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
        SELECT COUNT(id) AS total FROM orders o 
        WHERE o.artisan_id = %s AND o.display_seller = true;
        '''
        return sql
    
    @torndb.get
    def count_orders_by_seller_status(self, artisan_id, status):
        sql = '''
        SELECT COUNT(id) AS total FROM orders o 
        WHERE o.artisan_id = %s AND o.status = %s AND o.display_seller = true;
        '''
        return sql
    
    @torndb.select
    def find_orders_by_seller(self, artisan_id, max_results = 0, first_result = 10):
        sql = '''
        SELECT * FROM orders o 
        WHERE o.artisan_id = %s AND o.display_seller = true
        ORDER BY o.update_time DESC
        LIMIT %s OFFSET %s;
        '''
        return sql
    
    @torndb.select
    def find_orders_by_seller_status(self, artisan_id, status, max_results = 0, first_result = 10):
        sql = '''
        SELECT * FROM orders o 
        WHERE o.artisan_id = %s AND o.status = %s AND o.display_seller = true
        ORDER BY o.update_time DESC
        LIMIT %s OFFSET %s;
        '''
        return sql
    
    @torndb.get
    def count_orders_by_buyer(self, artisan_id):
        sql = '''
        SELECT COUNT(id) AS total FROM orders o 
        WHERE o.user_id = %s AND o.display_buyer = true;
        '''
            
        return sql
    
    @torndb.get
    def count_orders_by_buyer_status(self, artisan_id, status):
        sql = '''
        SELECT COUNT(id) AS total FROM orders o 
        WHERE o.user_id = %s AND o.status in %s AND o.display_buyer = true;
        '''
        return sql
    
    @torndb.select
    def find_orders_by_buyer(self, user_id, max_results = 0, first_result = 10):
        sql = '''
        SELECT * FROM orders o 
        WHERE o.user_id = %s AND o.display_buyer = true
        ORDER BY o.update_time DESC
        LIMIT %s OFFSET %s;
        '''
        return sql
    
    @torndb.select
    def find_orders_by_buyer_status(self, user_id, status, max_results = 0, first_result = 10):
        sql = '''
        SELECT * FROM orders o 
        WHERE o.user_id = %s AND o.status in %s AND o.display_buyer = true
        ORDER BY o.update_time DESC
        LIMIT %s OFFSET %s;
        '''
        return sql
    
    def process_params(self,buyer, seller, status, 
                              start_date, end_date):
        sql_params = list()
        params = dict()
        has_params = False
        if buyer != None:
            sql_params.append('o.user_id = %(user_id)s')
            params['user_id'] = buyer
            has_params = True
            
        if seller != None:
            sql_params.append('o.artisan_id = %(artisan_id)s')
            params['artisan_id'] = seller
            has_params = True
        
        if status != None:
            sql_params.append('o.status = %(status)s')
            params['status'] = status
            has_params = True
            
        if start_date != None:
            sql_params.append('o.create_time > %(start_date)s')
            params['start_date'] = start_date
            has_params = True
            
        if end_date != None:
            sql_params.append('o.create_time < %(end_date)s')
            params['end_date'] = end_date
            has_params = True
            
        return sql_params, params, has_params
    
    def count_orders_by_admin(self, buyer = None, seller = None, status = None, 
                              start_date = None, end_date = None):
        
        sql_params, params, has_params = self.process_params(buyer, seller, status, start_date, end_date)
        sql = '''
        SELECT COUNT(id) AS total FROM orders o
        '''
        if has_params:
            sql = '%s WHERE %s' % (sql, ' '.join(sql_params))
        
        hits = torndb.torcon.query(sql, **params)
        
        return hits
    
    def find_orders_by_admin(self, buyer = None, seller = None, status = None, 
                              start_date = None, end_date = None, max_results = 0, first_result = 10):
        sql_params, params, has_params = self.process_params(buyer, seller, status, start_date, end_date)
        params['first_result'] = first_result
        params['max_results'] = max_results
        sql = '''
        SELECT * FROM orders o
        '''
        if has_params:
            sql = '%s WHERE %s' % (sql, ' '.join(sql_params))
        sql = '%s ORDER BY o.update_time DESC LIMIT %%(max_results)s OFFSET %%(first_result)s' % (sql)
        orders = torndb.torcon.query(sql, **params)
        return orders
    
    @torndb.insert
    def save(self, **order):
        sql = '''
        INSERT INTO orders (user_id, buyer_avatar, buyer_name, address, 
        telephone, title, order_no, trade_no, status, create_time, 
        update_time, display_buyer, display_seller, is_reviewed, 
        artisan_id, artisan_name, artisan_avatar, sample_id, sample_name,sample_tag_price, 
        sample_price, sample_brief, cover, tag_price, price, remark) 
        VALUES (%(user_id)s, %(buyer_avatar)s, %(buyer_name)s, %(address)s, 
        %(telephone)s, %(title)s, %(order_no)s, 
        %(trade_no)s, %(status)s, %(create_time)s, 
        %(update_time)s, %(display_buyer)s, %(display_seller)s, 
        %(is_reviewed)s, %(artisan_id)s, %(artisan_name)s, %(artisan_avatar)s,
        %(sample_id)s, %(sample_name)s, %(sample_tag_price)s, %(sample_price)s, 
        %(sample_brief)s, %(cover)s, %(tag_price)s, %(price)s, %(remark)s);
        '''
        
        return sql
    
    @torndb.update
    def update(self, **order):
        sql = '''
        UPDATE orders SET status = %(status)s, update_time = %(update_time)s, 
        display_buyer = %(display_buyer)s, display_seller = %(display_seller)s, 
        is_reviewed = %(is_reviewed)s, tag_price = %(tag_price)s, price = %(price)s
        WHERE id = %(id)s;
        '''
        return sql
    
    @torndb.update
    def close_evaluate(self, close_time):
        sql = '''
        UPDATE orders SET is_reviewed = 2, update_time = now()
        WHERE order_no in (SELECT order_no FROM evaluate WHERE create_time < %s);
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
    
    def batch_save(self, orderLogs):
        params = list()
        for orderLog in orderLogs:
            params.append((orderLog['trader_id'],orderLog['trader_type'],
                           orderLog['trader_action'],orderLog['order_id'],orderLog['create_time']))
        sql = '''
        INSERT INTO order_log (trader_id, trader_type, trader_action, 
        order_id, create_time) 
        VALUES (%s, %s, %s, %s, %s);
        '''
        x = torndb.torcon.executemany(sql, params)
        
        return x
    
    @torndb.select
    def find(self, order_id):
        sql = '''
        SELECT * FROM order_log WHERE order_id = %s AND trader_action <> 7;
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
    @torndb.get
    def find(self, artisan_id, appt_date, appt_hour):
        sql = '''
        SELECT * FROM appointment WHERE artisan_id = %s AND appt_date = %s AND appt_hour = %s;
        '''
        return sql
    
    @torndb.select
    def find_day(self, artisan_id, appt_date):
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
    
    @torndb.delete
    def delete(self, order_no):
        sql = '''
        DELETE FROM appointment WHERE order_no = %s
        '''
        return sql
    
    @torndb.delete
    def batch_delete(self, order_nos):
        sql = '''
        DELETE FROM appointment WHERE order_no IN %s;
        '''
        return sql
    
appointmentDAO = AppointmentDAO()
