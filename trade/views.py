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
    @Api()
    def get(self):
        '''
        查看手艺人预约状态
        @param artisan_id: 手艺人ID
        @param appt_date: 预约日期 格式 2000-01-01
        '''
        artisan_id = self.get_argument('artisan_id', strip=True)
        appt_date = self.get_argument('appt_date', strip=True)
        appt_date = str2date(appt_date)
        apptss = trade_serv.appointment_status(artisan_id, appt_date);
        self.render_json(apptss)

@application.RequestMapping(r"/trade/create")
class CreateTrade(application.RequestHandler):
    @Api(auth=True)
    def post(self):
        '''
        创建订单
        @param sample_id: 样品ID
        @param address: 服务地址
        @param appt_date: 预约日期 格式 2000-01-01
        @param appt_hour: 预约时间
        @param remark: 用户备注
        '''
        user_id = self.user_id
        sample_id = self.get_argument('sample_id', strip=True)
        address = self.get_argument('address', strip=True)
        appt_date = self.get_argument('appt_date', strip=True)
        appt_date = str2date(appt_date)
        appt_hour = self.get_argument('appt_hour', strip=True)
        appt_hour = int(appt_hour)
        order_from = self.get_argument('order_from',default = None, strip=True)
        remark = self.get_argument('remark',default = None, strip=True)
#         order_from = None
#         order = dict(user_id = user_id)
        order = trade_serv.create_order(user_id, sample_id, address, appt_date, appt_hour, order_from, remark)
        self.render_json(order)
        
@application.RequestMapping(r"/trade/user")
class UserTrade(application.RequestHandler):
    '''
    用户交易操作：
    @param action: arrived, 用户确认手艺人已经到达; finish, 用户确认交易结束, cancel, 用户取消交易
    @param price: 实际费用
    '''
    @Api(auth=True)
    def post(self):
        user_id = self.user_id
        order_no = self.get_argument('order_no', strip=True)
        action = self.get_argument('action', default = "finish", strip=True)
        price = self.get_argument('price', default = None, strip=True)
        order = trade_serv.trade(user_id, order_no, action, price)
        
        self.render_json(order)
        
@application.RequestMapping(r"/trade/artisan")
class ArtisanTrade(application.RequestHandler):
    '''
    用户交易操作：
    @param action: send, 手艺人已出发;
    '''
    @Api(auth=True)
    def post(self):
        artisan_id = self.user_id
        order_no = self.get_argument('order_no', strip=True)
        action = self.get_argument('action', default = "send", strip=True)
        order = trade_serv.trade(artisan_id, order_no, action)
        
        self.render_json(order)
        
@application.RequestMapping(r"/order")
class OrderDetail(application.RequestHandler):
    @Api()
    def get(self):
        order_no = self.get_argument('order_no', strip=True)
        order = trade_serv.get_order_orderno(order_no)
        self.render_json(order)
        
@application.RequestMapping(r"/orders")
class Orders(application.RequestHandler):
    @Api(auth=True)
    def get(self):
        '''
        用户订单列表
        @param status: 订单状态（不选为全部）
        @param page: 
        @param page_size: 
        '''
        user_id = self.user_id
        status = self.get_argument('status', default = None, strip=True)
        page = self.get_argument('page', default = 1, strip=True)
        page = int(page)
        page_size = self.get_argument('page_size', default = 10, strip=True)
        page_size = int(page_size)
        order, hits = trade_serv.buyer_orders(user_id, status, page, page_size)
        self.render_json(order)
        
@application.RequestMapping(r"/remote/trade")
class RemoteTrade(application.RequestHandler):
    '''
    用户交易操作（remote）：
    @param action: arrived, 用户确认手艺人已经到达; finish, 用户确认交易结束, cancel, 用户取消交易
    @param price: 实际费用
    '''
    def post(self):
        user_id = self.get_argument('user_id', strip=True)
        order_no = self.get_argument('order_no', strip=True)
        action = self.get_argument('action', default = "finish", strip=True)
        price = self.get_argument('price', default = None, strip=True)
        order = trade_serv.trade(user_id, order_no, action, price)
        
        self.render_json(order)
        
@application.RequestMapping(r"/backend/artisan/trade")
class BackendArtisanTrade(application.RequestHandler):
    '''
    手艺人交易操作：
    @param action: send, 手艺人已出发;
    '''
    def post(self):
        artisan_id = self.get_current_user()['id']
        order_no = self.get_argument('order_no', strip=True)
        action = self.get_argument('action', default = "send", strip=True)
        order = trade_serv.trade(artisan_id, order_no, action)
        
        self.render('trade/order.html', order = order)
        
@application.RequestMapping(r"/backend/artisan/orders")
class BackendArtisanOrders(application.RequestHandler):
    '''
    手艺人交易操作：
    @param action: send, 手艺人已出发;
    '''
    def get(self):
        artisan_id = self.get_current_user()['id']
        status = self.get_argument('status', default = None, strip=True)
        page = self.get_argument('page', default = 1, strip=True)
        page = int(page)
        page_size = self.get_argument('page_size', default = 10, strip=True)
        page_size = int(page_size)
        orders, hits = trade_serv.seller_orders(artisan_id, status, page, page_size)
        self.render('trade/artisan_orders.html', orders = orders, 
                    page=page, page_size=page_size, total=hits, status_description = trade_serv.order_status_description
                    )
        
@application.RequestMapping(r"/backend/orders")
class BackenAdminOrders(application.RequestHandler):
    def get(self):
        '''
        用户订单列表
        @param status: 订单状态（不选为全部）
        @param page: 
        @param page_size: 
        '''
        buyer = self.get_argument('buyer', default = None, strip=True)
        seller = self.get_argument('seller', default = None, strip=True)
        start_date = self.get_argument('start_date', default = None, strip=True)
        end_date = self.get_argument('end_date', default = None, strip=True)
        status = self.get_argument('status', default = None, strip=True)
        page = self.get_argument('page', default = 1, strip=True)
        page = int(page)
        page_size = self.get_argument('page_size', default = 10, strip=True)
        page_size = int(page_size)
        orders, hits = trade_serv.admin_orders(buyer, seller, status, start_date, end_date, page, page_size)
        print orders
        self.render('trade/admin_orders.html', orders = orders, 
                    page=page, page_size=page_size, total=hits, status_description = trade_serv.order_status_description
                    )