# -*- coding:utf-8 -*-
'''
Created on Mar 4, 2015

@author: zhuhua
'''
from simpletor import application
from alipay import sign_type, alipay

@application.RequestMapping('/pay_notify/alipay')
class AliNotify(application.RequestHandler):
    
    def get(self):
        out_trade_no = self.get_argument('out_trade_no', strip=True) #商户订单号
        trade_no = self.get_argument('trade_no', strip=True) #支付宝交易号
        trade_status = self.get_argument('trade_status', strip=True) #交易状态
        
        if self.verify():
            if trade_status == 'TRADE_FINISHED':
                pass
                #判断该笔订单是否在商户网站中已经做过处理
                #如果没有做过处理，根据订单号（out_trade_no）在商户网站的订单系统中查到该笔订单的详细，并执行商户的业务程序
                #如果有做过处理，不执行商户的业务程序
                
                #注意：
                #该种交易状态只在两种情况下出现
                #1、开通了普通即时到账，买家付款成功后。
                #2、开通了高级即时到账，从该笔交易成功时间算起，过了签约时的可退款时限（如：三个月以内可退款、一年以内可退款等）后。
            elif trade_status == 'TRADE_SUCCESS':
                pass
                #判断该笔订单是否在商户网站中已经做过处理
                #如果没有做过处理，根据订单号（out_trade_no）在商户网站的订单系统中查到该笔订单的详细，并执行商户的业务程序
                #如果有做过处理，不执行商户的业务程序
                
                #注意：
                #该种交易状态只在一种情况下出现——开通了高级即时到账，买家付款成功后。
            
            self.write('success')
            
        self.finish()
        
    def verify(self):
        params = self.request.arguments
        response_txt = 'true'
        if params.get('notify_id') is not None:
            notify_id = params.get('notify_id')[0]
            response_txt = alipay.verify_response(notify_id)
            
        sign = ''
        if params.get('sign') is not None:
            sign = params.get('sign')[0]
            
        is_sign = self.get_sign_veryfy(params, sign)

        if is_sign and response_txt == 'true':
            return True
        else:
            return False
        
    def get_sign_veryfy(self, params, sign):
        #过滤空值、sign与sign_type参数
        params = alipay.para_filter(params)
        #获取待签名字符串
        pre_sign_str = alipay.create_link_string(params)
        #获得签名验证结果
        is_sign = False
        if sign_type == 'RSA':
            is_sign = alipay.verify(pre_sign_str, sign)
            
        return is_sign