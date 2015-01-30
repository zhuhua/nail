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
        self.status = None
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
        self.date = None
        self.hour = None
        
class OrderDAO:
    '''
    订单数据访问接口
    '''
    @torndb.get
    def find(self, order_id):
        sql = '''
        SELECT * FROM order o WHERE o.id = %s;
        '''
        return sql
    
    @torndb.select
    def all(self):
        sql = '''
        SELECT * FROM category;
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