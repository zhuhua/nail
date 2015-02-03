# -*- coding:utf-8 -*-
'''
Created on Jan 28, 2015

@author: lisong
'''
from simpletor.torndb import transactional
from simpletor.application import AppError
# from simpletor.tornsolr import index, connect
from simpletor.utils import validate_utils, generate_order_no
from common import services as common_serv
from artisan import services as artisan_serv
from sample import services as sample_serv
from user import services as user_serv

import models
import settings
from datetime import date, datetime

order_status_description = ('未支付','已支付', '出发', '到达', '完成')
order_operate_description = ('pay', 'send', 'arrived', 'finish')

def appointment_status(artisan_id, appt_date):
    if appt_date < date.today():
        raise AppError("超出可预约时间范围")
    appts = models.appointmentDAO.find(artisan_id, appt_date);
    appt_hours = list()
    appt_status = dict()
    appt_status['artisan_id'] = artisan_id
    appt_status['appt_date'] = appt_date
    for a in appts:
        appt_hours.append(a.appt_hour)
    for x in range(settings.appointmentRange[0], settings.appointmentRange[1] + 1):
        status = True
        if x in appt_hours:
            status = False
        appt_status[x] = status

    return appt_status

@transactional
def close_appointment(artisan_id, appt_date, appt_hour):
    if appt_hour < settings.appointmentRange[0] or appt_hour > settings.appointmentRange[1]:
        raise AppError("超出可预约时间范围")
    appt = models.Appointment()
    appt.artisan_id = artisan_id
    appt.appt_date = appt_date
    appt.appt_hour = appt_hour
    
    models.appointmentDAO.save(**appt)

@transactional
def create_order(user_id, sample_id, order_from, address, appt_date, appt_hour):
    if appt_date < date.today() or appt_hour < settings.appointmentRange[0] or appt_hour > settings.appointmentRange[1]:
        raise AppError("超出可预约时间范围")
    
    user = user_serv.get_profile(user_id)
    sample = sample_serv.get_sample(sample_id)
    if sample == None:
        raise AppError("作品不存在(id:%s)" % (sample_id))
    
    artisan_id = sample.artisan_id
    artisan = artisan_serv.get_artisan(artisan_id)
    if artisan == None:
        raise AppError("手艺人不存在(id:%s)" % (artisan_id))
    order = models.Order()
    order.address = address
    order.artisan_id = sample.artisan_id
    order.artisan_name = artisan.name
    order.buyer_name = user.nick
    order.cover = sample.images[0]
    order.create_time = datetime.now()
    order.display_buyer = True
    order.display_seller = True
    order.is_reviewed = False
    order_no = generate_order_no()
    order.order_no = order_no
    order.price = sample.price
    order.sample_id = sample_id
    order.sample_name = sample.name
    order.status = 0;
    order.tag_price = sample.tag_price
    order.telephone = user.mobile
    order.title = sample.name
    order.trade_no = generate_order_no()
    order.update_time = datetime.now()
    order.user_id = user_id
    
    models.orderDAO.save(**order)
    
    return get_order_orderno(order_no)
    
def get_order(order_id):
    return models.orderDAO.find(order_id)

def get_order_orderno(order_no):
    return models.orderDAO.find_by_order_no(order_no)

def seller_orders(artisan_id, status = None, page = 1, page_size = 10):
    first_result = (page - 1) * page_size
        # 卖家订单
    total = models.orderDAO.count_orders_by_seller(artisan_id)
    orders = models.orderDAO.find_orders_by_seller(artisan_id, page_size, first_result)
    
    return orders, total

def buyer_orders(user_id, status = None, page = 1, page_size = 10):
    first_result = (page - 1) * page_size
        # 买家 状态订单
    total = models.orderDAO.count_orders_by_buyer(user_id, status)
    orders = models.orderDAO.find_orders_by_buyer(user_id, status, page_size, first_result)
    
    return orders, total

def admin_orders(buyer = None, seller = None, status = None, start_date = None, end_date = None, page = 1, page_size = 10):
    first_result = (page - 1) * page_size
    total = models.orderDAO.count_orders_by_admin(buyer, seller, status, start_date, end_date)
    orders = models.orderDAO.find_orders_by_admin(buyer, seller, status, start_date, end_date, page_size, first_result)
    
    return orders, total
    
    
