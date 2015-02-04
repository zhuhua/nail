# -*- coding:utf-8 -*-
'''
Created on Jan 28, 2015

@author: lisong
'''
import datetime
from simpletor import application
from simpletor.utils import str2date
from api import Api
from trade import services as trade_serv

@application.RequestMapping("/appointment/status")
class ApptStatus(application.RequestHandler):
    
    def get(self):
        artisan_id = self.get_argument('artisan_id', strip=True)
        appt_date = self.get_argument('appt_date', strip=True)
        appt_date = str2date(appt_date)
        apptss = trade_serv.appointment_status(artisan_id, appt_date);
        self.render_json(apptss)


@application.RequestMapping("/trade/create")
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

@application.RequestMapping("/order")
class List(application.RequestHandler):
    def get(self):
        order_no = self.get_argument('order_no', strip=True)
#         order_no = str(order_no)
#         order_id = self.get_argument('order_id',default = None, strip=True)
        order = trade_serv.get_order_orderno(order_no)
        self.render_json(order)