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

order_status_description = (u'待支付',u'已支付', u'已出发', u'已到达', u'已完成',
                             u'已取消', u'已关闭', u'已过期')
order_action_description = ('create', 'pay', 'send', 'arrived', 'finish', 'cancel', 'close','expire')
order_trader_type = dict(user = 'USER', artisan = 'ARTISAN', system = 'SYSTEM')
order_status_group = dict(wait_pay=[0,0], unfinished=[1,2,3], finished=[4, 4], other=[5,6,7])

def appointment_status(artisan_id, appt_date):
    appts = appointmentDAO.find_day(artisan_id, appt_date);
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
        if (appt_date <= date.today() and x < datetime.now().time().hour):
            status = False
        appt_status[x] = status

    return appt_status

def artisan_appt_status(artisan_id, appt_date):
    appts = appointmentDAO.find_day(artisan_id, appt_date);
    appt_status = dict()
    for a in appts:
        a['status'] = 1
        appt_status[a.appt_hour] = a
        
    for x in range(settings.appointmentRange[0], settings.appointmentRange[1] + 1):
        if appt_status.has_key(x):
            pass
        elif (appt_date <= date.today() and x < datetime.now().time().hour):
            appt_status[x] = dict(status = -1)
        else:
            appt_status[x] = dict(status = 0)
            
    return appt_status

@transactional
def close_appointment(artisan_id, appt_date, appt_hour):
    if appt_hour < settings.appointmentRange[0] or appt_hour > settings.appointmentRange[1]:
        raise AppError(u"超出可预约时间范围")
    appt = models.Appointment()
    appt.artisan_id = artisan_id
    appt.appt_date = appt_date
    appt.appt_hour = appt_hour
    
    apptx = appointmentDAO.find(artisan_id, appt_date, appt_hour)
    if apptx != None:
        raise AppError(u"时间已经预约")
    try:
        appointmentDAO.save(**appt)
    except Exception, e:
        print e
        raise AppError(u"时间范围不可预约")

@transactional
def create_order(user_id, sample_id, address, appt_date, appt_hour, order_from = None, remark = None):
    is_notcorrect_hour = appt_hour < settings.appointmentRange[0]
    is_notcorrect_hour = is_notcorrect_hour or appt_hour > settings.appointmentRange[1]
    is_notcorrect_date = appt_date < date.today()
    if appt_date == date.today:
        is_notcorrect_hour = is_notcorrect_hour or datetime.now().time().hour > appt_hour
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
    order.artisan_avatar = artisan.avatar
    order.buyer_name = user.nick
    order.buyer_avatar = user.avatar
    if len(sample.images) > 0:
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
    status = int(order.status)
    orderLog = models.OrderLog()
#     orderLog.create_time 
    orderLog.order_id = order.id
    orderLog.trader_action = order_action_description.index(action)
    orderLog.trader_id = trader_id
    real_trade_id = None
    if order_action_description.index(action) == order_action_description.index('pay'):#用户进行支付操作
        wait_pay_status = order_status_description.index(u'待支付')
        expired_status = order_status_description.index(u'已过期')
        if status != wait_pay_status and status != expired_status: #订单为未支付状态
            
            raise AppError(u"订单不支持支付操作")
        order.status = order_status_description.index(u'已支付')
        order.update_time = datetime.now()
        orderLog.trader_type = order_trader_type['user']
        real_trade_id = order.user_id
    elif order_action_description.index(action) == order_action_description.index('send'):#手艺人出发
        if status != order_status_description.index(u'已支付'): #订单为未支付状态
            raise AppError(u"订单不支持出发操作")
        order.status = order_status_description.index(u'已出发')
        order.update_time = datetime.now()
        orderLog.trader_type = order_trader_type['artisan']
        real_trade_id = order.artisan_id
    elif order_action_description.index(action) == order_action_description.index('arrived'):#用户确认手艺人到达
        if status != order_status_description.index(u'已出发'): #订单为未支付状态
            raise AppError(u"订单不支持到达操作")
        order.status = order_status_description.index(u'已到达')
        order.update_time = datetime.now()
        orderLog.trader_type = order_trader_type['user']
        real_trade_id = order.user_id
    elif order_action_description.index(action) == order_action_description.index('finish'):#用户确认交易结束
        if status != order_status_description.index(u'已到达'): #订单为未支付状态
            raise AppError(u"订单不支持完成操作")
        order.status = order_status_description.index(u'已完成')
        order.update_time = datetime.now()
        orderLog.trader_type = order_trader_type['user']
        real_trade_id = order.user_id
    elif order_action_description.index(action) == order_action_description.index('cancel'):#用户取消订单
        if status != order_status_description.index(u'待支付'): #订单为未支付状态
            raise AppError(u"订单不支持取消操作")
        order.status = order_status_description.index(u'已取消')
        order.update_time = datetime.now()
        orderLog.trader_type = order_trader_type['user']
        real_trade_id = order.user_id
    elif order_action_description.index(action) == order_action_description.index('close'):#系统关闭
        if status != order_status_description.index(u'待支付'): #订单为未支付状态
            raise AppError(u"订单不支持关闭操作")
        order.status = order_status_description.index(u'已关闭')
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
def batch_expire(expire_time):
    orders_ids = orderDAO.find_expire(expire_time)
    orders = list();
    orderLogs = list()
    for x in orders_ids:
        order_id = x['id']
        orders.append(order_id)
        
        orderLog = models.OrderLog()
#     orderLog.create_time 
        orderLog.order_id = order_id
        orderLog.trader_action = order_action_description.index('expire')
        orderLog.trader_id = -1
        orderLog.trader_type = order_trader_type['system']
        orderLogs.append(orderLog)
        
    orderDAO.execute_expire(order_status_description.index(u'已过期'), orders)
    orderLogDAO.batch_save(orderLogs)
    
@transactional
def review(order_no, user_id):
    order = get_order_orderno(order_no)
    user_id = int(user_id)
    if order.is_reviewed == 1:
        raise AppError(u"订单已评价")
    if order.user_id != user_id:
        raise AppError(u"评价订单操作用户错误")
    if order.status != order_status_description.index(u'已完成'):
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
        
    add_order_remain(order)
    return order

def get_order_orderno(order_no, with_log = False):
    order = models.orderDAO.find_by_order_no(order_no)
    if order == None:
        message = u"订单不存在(order_no:%s)" % (order_no)
        raise AppError(message)
    
    if with_log:
        order.order_log = models.orderLogDAO.find(order.id)
    
    add_order_remain(order)
    return order

def delete_order(order_id, user_id):
    order = get_order(order_id)
    if order.user_id != int(user_id):
        raise AppError(u"订单不属于此用户")
    if not (order.status in (0, 4, 5, 6)):
        raise AppError(u"订单不能删除")
    order.display_buyer = 0
    order.update_time = datetime.now()
    
    models.orderDAO.update(**order)

    return order

def delete_order_artisan(order_id, artisan_id):
    order = get_order(order_id)
    if order.artisan_id != int(artisan_id):
        raise AppError(u"订单不属于此用户")
    if not (order.status in (4,)):
        raise AppError(u"订单不能删除")
    order.display_seller = 0
    order.update_time = datetime.now()
    
    models.orderDAO.update(**order)
    
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
    
    for order in orders:
        add_order_remain(order)
        
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
        status = order_status_group[status]
        if status == None:
            raise AppError(u'订单状态错误')
        print status
        total = models.orderDAO.count_orders_by_buyer_status(user_id, status)
        orders = models.orderDAO.find_orders_by_buyer_status(user_id, status, page_size, first_result)
    
    for order in orders:
        add_order_remain(order)
        
    return orders, total['total']

def admin_orders(buyer = None, seller = None, status = None, start_date = None, end_date = None, page = 1, page_size = 10):
    first_result = (page - 1) * page_size
    total = models.orderDAO.count_orders_by_admin(buyer, seller, status, start_date, end_date)
    orders = models.orderDAO.find_orders_by_admin(buyer, seller, status, start_date, end_date, page_size, first_result)
    
    for order in orders:
        add_order_remain(order)
        
    return orders, total[0]['total']
    
def add_order_remain(order):
    remain = settings.order_expire_time - ((datetime.now() - order.create_time).seconds / 60)
    if remain < 0:
        remain = 0
    order.expire_remian = remain
    return order