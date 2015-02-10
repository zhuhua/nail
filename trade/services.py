# -*- coding:utf-8 -*-
'''
Created on Jan 28, 2015

@author: lisong
'''
from datetime import date, datetime
from simpletor.torndb import transactional
from simpletor.application import AppError
# from simpletor.tornsolr import index, connect
from simpletor.utils import generate_order_no #validate_utils,
# from common import services as common_serv
from artisan import services as artisan_serv
from sample import services as sample_serv
from user import services as user_serv

import models
from models import appointmentDAO, orderDAO, orderLogDAO
import settings

order_status_description = ('待支付','已支付', '已出发', '已到达', '已完成', '已取消', '已关闭')
order_action_description = ('create', 'pay', 'send', 'arrived', 'finish', 'cancel', 'close')
order_trader_type = dict(user = 'USER', artisan = 'ARTISAN', system = 'SYSTEM')

def appointment_status(artisan_id, appt_date):
    appts = appointmentDAO.find(artisan_id, appt_date);
    appt_hours = list()
    appt_status = dict()
#     appt_status['artisan_id'] = artisan_id
#     appt_status['appt_date'] = appt_date
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
        raise AppError(u"超出可预约时间范围")
    appt = models.Appointment()
    appt.artisan_id = artisan_id
    appt.appt_date = appt_date
    appt.appt_hour = appt_hour
    try:
        appointmentDAO.save(**appt)
    except Exception, e:
        raise AppError(u"时间范围不可预约")

@transactional
def create_order(user_id, sample_id, address, appt_date, appt_hour, order_from = None, remark = None):
    is_notcorrect_date = appt_date < date.today()
    is_notcorrect_hour = datetime.now().time().hour > appt_hour
    is_notcorrect_hour = is_notcorrect_hour or appt_hour < settings.appointmentRange[0]
    is_notcorrect_hour = is_notcorrect_hour or appt_hour > settings.appointmentRange[1]
    if is_notcorrect_date or is_notcorrect_hour:
        raise AppError(u"超出可预约时间范围")
    
    user = user_serv.get_profile(user_id)
    sample = sample_serv.get_sample(sample_id)
    if sample == None:
        raise AppError(u"作品不存在(id:%s)" % (sample_id))
    
    artisan_id = sample.artisan_id
    artisan = artisan_serv.get_artisan(artisan_id)
    if artisan == None:
        raise AppError(u"手艺人不存在(id:%s)" % (artisan_id))
    #设定预约
    close_appointment(artisan_id, appt_date, appt_hour)
    
    order = models.Order()
    order.address = address
    order.artisan_id = sample.artisan_id
    order.artisan_name = artisan.name
    order.buyer_name = user.nick
    order.cover = sample.images[0]
#     order.create_time = datetime.now()
#     order.display_buyer = True
#     order.display_seller = True
#     order.is_reviewed = False
    order_no = generate_order_no()
    order.order_no = order_no
    order.price = sample.price
    order.remark = remark
    order.sample_id = sample_id
    order.sample_name = sample.name
    order.sample_tag_price = sample.tag_price
    order.sample_price = sample.price# from simpletor.utils import validate_utils, generate_order_no
# from common import services as common_serv
#     order.status = 0;
    order.tag_price = sample.tag_price
    order.telephone = user.mobile
    order.title = sample.name
    order.trade_no = generate_order_no()
#     order.update_time = datetime.now()
    order.user_id = user_id
    
    orderDAO.save(**order)
    order = get_order_orderno(order_no)
    orderLog = models.OrderLog()
    orderLog.order_id = order.id
    orderLog.trader_action = order_action_description.index('create')
    orderLog.trader_id = user_id
    orderLog.trader_type = order_trader_type['user']
#     orderLog.create_time
    orderLogDAO.save(**orderLog)
    
    return order

@transactional
def trade(trader_id, order_no, action, price = None):
    order = get_order_orderno(order_no)
    status = order.status
    orderLog = models.OrderLog()
#     orderLog.create_time 
    orderLog.order_id = order.id
    orderLog.trader_action = order_action_description.index(action)
    orderLog.trader_id = trader_id
    real_trade_id = None
    if order_action_description.index(action) == order_action_description.index('pay'):#用户进行支付操作
        if status != order_status_description.index('待支付'): #订单为未支付状态
            raise AppError(u"订单不支持支付操作")
        order.status = order_status_description.index('已支付')
        order.update_time = datetime.now()
        orderLog.trader_type = order_trader_type['user']
        real_trade_id = order.user_id
    elif order_action_description.index(action) == order_action_description.index('send'):#手艺人出发
        if status != order_status_description.index('已支付'): #订单为未支付状态
            raise AppError(u"订单不支持出发操作")
        order.status = order_status_description.index('已出发')
        order.update_time = datetime.now()
        orderLog.trader_type = order_trader_type['artisan']
        real_trade_id = order.artisan_id
    elif order_action_description.index(action) == order_action_description.index('arrived'):#用户确认手艺人到达
        if status != order_status_description.index('已出发'): #订单为未支付状态
            raise AppError(u"订单不支持到达操作")
        order.status = order_status_description.index('已到达')
        order.update_time = datetime.now()
        orderLog.trader_type = order_trader_type['user']
        real_trade_id = order.user_id
    elif order_action_description.index(action) == order_action_description.index('finish'):#用户确认交易结束
        if status != order_status_description.index('已到达'): #订单为未支付状态
            raise AppError(u"订单不支持完成操作")
        order.status = order_status_description.index('已完成')
        order.update_time = datetime.now()
        orderLog.trader_type = order_trader_type['user']
        real_trade_id = order.user_id
    elif order_action_description.index(action) == order_action_description.index('cancel'):#用户取消订单
        if status != order_status_description.index('待支付'): #订单为未支付状态
            raise AppError(u"订单不支持取消操作")
        order.status = order_status_description.index('已取消')
        order.update_time = datetime.now()
        orderLog.trader_type = order_trader_type['user']
        real_trade_id = order.user_id
    elif order_action_description.index(action) == order_action_description.index('close'):#系统关闭
        if status != order_status_description.index('待支付'): #订单为未支付状态
            raise AppError(u"订单不支持关闭操作")
        order.status = order_status_description.index('已关闭')
        order.update_time = datetime.now()
        orderLog.trader_type = order_trader_type['system']
        real_trade_id = None
    else:
        raise AppError(u"订单操作错误")
    
    if real_trade_id != None and real_trade_id != long(trader_id):
        raise AppError(u"订单操作用户错误")
    models.orderDAO.update(**order)
    models.orderLogDAO.save(**orderLog)
    order = get_order(order.id)
    return order

@transactional
def review(order_no, user_id):
    order = get_order_orderno(order_no)
    user_id = int(user_id)
    if order.is_reviewed == 1:
        raise AppError(u"订单已评价")
    if order.user_id != user_id:
        raise AppError(u"评价订单操作用户错误")
    if order.status != order_status_description.index('已完成'):
        raise AppError('订单未成功不能评价', field='order_no')
    order.is_reviewed = 1
    
    models.orderDAO.update(**order)
    
    return get_order(order.id, with_log = True)

def get_order(order_id, with_log = False):
    order = models.orderDAO.find(order_id)
    if order == None:
        raise AppError(u"订单不存在(id:%s)" % (order_id))
    if with_log:
        order.order_log = models.orderLogDAO.find(order.id)
    return order

def get_order_orderno(order_no, with_log = False):
    order = models.orderDAO.find_by_order_no(order_no)
    if order == None:
        message = u"订单不存在(order_no:%s)" % (order_no)
        raise AppError(message)
    if with_log:
        order.order_log = models.orderLogDAO.find(order.id)
        
    return order

def seller_orders(artisan_id, status, page = 1, page_size = 10):
    first_result = (page - 1) * page_size
        # 卖家订单
    orders = None
    total = 0
    if status == None:
        total = models.orderDAO.count_orders_by_seller(artisan_id)
        orders = models.orderDAO.find_orders_by_seller(artisan_id, page_size, first_result)
    else:
        total = models.orderDAO.count_orders_by_seller_status(artisan_id, status)
        orders = models.orderDAO.find_orders_by_seller_status(artisan_id, status, page_size, first_result)
    
    return orders, total['total']

def buyer_orders(user_id, status, page = 1, page_size = 10):
    first_result = (page - 1) * page_size
        # 买家 状态订单
    orders = None
    total = 0
    if status == None:
        total = models.orderDAO.count_orders_by_buyer(user_id)
        orders = models.orderDAO.find_orders_by_buyer(user_id, page_size, first_result)
    else:
        total = models.orderDAO.count_orders_by_buyer_status(user_id, status)
        orders = models.orderDAO.find_orders_by_buyer_status(user_id, status, page_size, first_result)
    
    return orders, total['total']

def admin_orders(buyer = None, seller = None, status = None, start_date = None, end_date = None, page = 1, page_size = 10):
    first_result = (page - 1) * page_size
    total = models.orderDAO.count_orders_by_admin(buyer, seller, status, start_date, end_date)
    orders = models.orderDAO.find_orders_by_admin(buyer, seller, status, start_date, end_date, page_size, first_result)
    
    return orders, total[0]['total']
    
    
