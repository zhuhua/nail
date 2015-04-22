# -*- coding:utf-8 -*-
'''
Created on Apr 3, 2015

@author: lisong
'''
import datetime
from simpletor.torndb import transactional
from trade import models as trade_models

close_time = datetime.datetime.now() - datetime.timedelta(days = 15)

@transactional
def close():
    x = trade_models.orderDAO.close_evaluate(close_time)
    
    print 'processed %s record(s) at %s' % (x, datetime.datetime.now())
    
if __name__ == '__main__':
    close()