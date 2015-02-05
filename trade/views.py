# -*- coding:utf-8 -*-
'''
Created on Jan 28, 2015

@author: lisong
'''
from simpletor import application
from simpletor.utils import str2date
from api import Api
from trade import services as trade_serv

@application.RequestMapping(r"/appointment/status")
class ApptStatus(application.RequestHandler):
    
    def get(self):
        artisan_id = self.get_argument('artisan_id', strip=True)
        appt_date = self.get_argument('appt_date', strip=True)
        appt_date = str2date(appt_date)
        apptss = trade_serv.appointment_status(artisan_id, appt_date);
        self.render_json(apptss)

@application.RequestMapping(r"/trade/create")
class CreateTrade(application.RequestHandler):
    @Api
    def post(self):
        user_id = self.user_id
        sample_id = self.get_argument('sample_id', strip=True)
        address = self.get_argument('address', strip=True)
        appt_date = self.get_argument('appt_date', strip=True)
        appt_hour = self.get_argument('appt_hour', strip=True)
        order_from = self.get_argument('order_from',default = None, strip=True)
        remark = self.get_argument('remark',default = None, strip=True)
        order = trade_serv.create_order(user_id, sample_id, address, appt_date, appt_hour, order_from, remark)
        self.renderjson(order)
        
@application.RequestMapping(r"/trade/user")
class UserTrade(application.RequestHandler):
    '''
    用户交易操作：
    @param action: arrived, 用户确认手艺人已经到达; finish, 用户确认交易结束
    @param price: 实际费用
    '''
    @Api
    def post(self):
        user_id = self.user_id
        order_no = self.get_argument('order_no', strip=True)
        action = self.get_argument('action', default = "finish", strip=True)
        price = self.get_argument('price', default = None, strip=True)
        order = trade_serv.trade(user_id, order_no, action, price)
        
        self.render_json(order)
        
@application.RequestMapping(r"/remote/trade")
class RemoteTrade(application.RequestHandler):
    '''
    用户交易操作：
    @param action: arrived, 用户确认手艺人已经到达; finish, 用户确认交易结束
    @param price: 实际费用
    '''
    def post(self):
        user_id = self.get_argument('user_id', strip=True)
        order_no = self.get_argument('order_no', strip=True)
        action = self.get_argument('action', default = "finish", strip=True)
        price = self.get_argument('price', default = None, strip=True)
        order = trade_serv.trade(user_id, order_no, action, price)
        
        self.render_json(order)
        
@application.RequestMapping(r"/backend/trade/artisan")
class BackendArtisanTrade(application.RequestHandler):
    '''
    用户交易操作：
    @param action: send, 手艺人已出发;
    '''
    def post(self):
        artisan_id = self.get_current_user()['id']
        order_no = self.get_argument('order_no', strip=True)
        action = self.get_argument('action', default = "send", strip=True)
        order = trade_serv.trade(artisan_id, order_no, action)
        
        self.render('template_name.html', order = order)

@application.RequestMapping(r"/trade/artisan")
class ArtisanTrade(application.RequestHandler):
    '''
    用户交易操作：
    @param action: send, 手艺人已出发;
    '''
    @Api
    def post(self):
        artisan_id = self.user_id
        order_no = self.get_argument('order_no', strip=True)
        action = self.get_argument('action', default = "send", strip=True)
        order = trade_serv.trade(artisan_id, order_no, action)
        
        self.render_json(order)
        
@application.RequestMapping(r"/order")
class OrderDetail(application.RequestHandler):
    def get(self):
        order_no = self.get_argument('order_no', strip=True)
        order = trade_serv.get_order_orderno(order_no)
        self.render_json(order)