# -*- coding:utf-8 -*-
'''
Created on Mar 3, 2015

@author: lisong
'''
from settings import order_expire_time
from trade.models import orderDAO
import datetime

if __name__ == '__main__':
    print order_expire_time
    expire_time = datetime.datetime.now() + datetime.timedelta(minutes = order_expire_time)
    print expire_time
    print orderDAO.count_expire(expire_time)