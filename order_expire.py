# -*- coding:utf-8 -*-
'''
Created on Mar 3, 2015

@author: lisong
'''
from settings import order_expire_time
from trade.models import orderDAO
from trade import services as trade_serv
import datetime

expire_time = datetime.datetime.now() + datetime.timedelta(minutes = order_expire_time)
def get_amount():
    return orderDAO.count_expire(expire_time)

def process_expired_orders():
    pass
    #查询已经过期的订单数量
    order_amount = get_amount()
    print 'found %s expired order(s)!' % order_amount['total']
    #查出过期订单ID，并将订单置为己过期状态，添加日志
    trade_serv.batch_expire(expire_time)
    
    print 'expire worker finished!'
    
if __name__ == '__main__':
    process_expired_orders()
