# -*- coding:utf-8 -*-
'''
Created on Mar 4, 2015

@author: zhuhua
'''
from simpletor import application
from alipay import sign_type, alipay
from trade import services as order_serv
from pay.wxpay import wxpay
import logging
from api import Api
from simpletor.application import AppError

log = logging.getLogger(__name__)

def trade_order(out_trade_no):
    order = order_serv.get_order_tradeno(out_trade_no)
    if order.status == order_serv.order_status_description.index(u'待支付'):
        try:
            order = order_serv.trade(order.user_id, order.order_no, 'pay')
        except Exception, e:
            print e
            
@application.RequestMapping('/pay_notify/alipay')
class AliNotify(application.RequestHandler):
    
    def post(self):
        out_trade_no = self.get_argument('out_trade_no', strip=True) #商户订单号
#         trade_no = self.get_argument('trade_no', strip=True) #支付宝交易号
        trade_status = self.get_argument('trade_status', strip=True) #交易状态
        
        if self.verify():
            if trade_status == 'TRADE_FINISHED':
                #判断该笔订单是否在商户网站中已经做过处理
               
                #如果没有做过处理，根据订单号（out_trade_no）在商户网站的订单系统中查到该笔订单的详细，并执行商户的业务程序
                #如果有做过处理，不执行商户的业务程序
                trade_order(out_trade_no)
                #注意：
                #该种交易状态只在两种情况下出现
                #1、开通了普通即时到账，买家付款成功后。
                #2、开通了高级即时到账，从该笔交易成功时间算起，过了签约时的可退款时限（如：三个月以内可退款、一年以内可退款等）后。
            elif trade_status == 'TRADE_SUCCESS':
                #判断该笔订单是否在商户网站中已经做过处理
                #如果没有做过处理，根据订单号（out_trade_no）在商户网站的订单系统中查到该笔订单的详细，并执行商户的业务程序
                #如果有做过处理，不执行商户的业务程序
                trade_order(out_trade_no)
                #注意：
                #该种交易状态只在一种情况下出现——开通了高级即时到账，买家付款成功后。
            
            self.write('success')
            
        self.finish()
        
    def verify(self):
        params = self.request.arguments
        log.debug(params)
        response_txt = 'true'
        if params.get('notify_id') is not None:
            notify_id = params.get('notify_id')[0]
            response_txt = alipay.verify_response(notify_id)
            
        sign = ''
        if params.get('sign') is not None:
            sign = params.get('sign')[0]
            
        is_sign = self.get_sign_veryfy(params, sign)
        
        if is_sign and response_txt == 'true':
            log.debug('Alipay verify success')
            return True
        else:
            log.debug('Alipay verify failed')
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

@application.RequestMapping('/f/')
class WxNotify(application.RequestHandler):
    '''
    微信支付回调地址
    '''
    def get(self):
        log.debug('tes url for weixin pay!')
        self.finish('success')
        
    def post(self):
        
        is_sign, params = self.verify()
        if is_sign:
            out_trade_no = params.get('out_trade_no')
            trade_order(out_trade_no)
            res = wxpay.dump_xml(dict(return_code='success', return_msg='ok'))
            self.write(res)
        self.finish()
        
    def verify(self):
        content = self.request.body
        logging.debug(content)
        params = wxpay.parse_xml(content)
        return_code = params.get('return_code').encode('utf-8')
        if return_code.lower() != 'success':
            return False
        result_code = params.get('result_code').encode('utf-8')
        if result_code.lower() != 'success':
            return False
        sign = ''
        if params.has_key('sign') is not None:
            sign = params.pop('sign')
            
        is_sign = self.get_sign_veryfy(params, sign)

        return is_sign, params
        
    def get_sign_veryfy(self, params, sign):
        #过滤空值、sign与sign_type参数
        params = wxpay.para_filter(params)
        #获取待签名字符串
        pre_sign_str = wxpay.create_link_string(params)
        #获得签名验证结果
        is_sign = wxpay.verify(pre_sign_str, sign)
            
        return is_sign
    
@application.RequestMapping('/api/wxpay/signture')
class WxSignture(application.RequestHandler):
    '''
    微信支付统一下单
    '''
    @Api()
    def get(self):
        user_id = None
        try:
            user_id = self.user_id
        except:
            pass
        #微信支付分配的终端设备号，商户自定义(非必要)
        signOnServer = self.get_argument('sign_on_server', default = None, strip=True)
        device_info = self.get_argument('device_info', default = None, strip=True)
        #符合ISO 4217标准的三位字母代码，默认人民币：CNY (非必要)
        fee_type = self.get_argument('fee_type', default = 'CNY', strip=True)
        #取值如下：JSAPI，NATIVE，APP(非必要 当前为APP)
        trade_type = self.get_argument('trade_type', default = 'APP', strip=True)
        #trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义。(有条件必要)
        product_id = self.get_argument('product_id', default = None, strip=True)
        #trade_type=JSAPI，此参数必传，用户在商户appid下的唯一标识(有条件必要)
        openid = self.get_argument('openid', default = None, strip=True) 
        #APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP
        #
        order_no = self.get_argument('order_no', strip=True)
        logging.debug(self.request.headers.get('X-Real-IP'))
#         logging.debug(dir(self.request))
#         logging.debug(self.request.headers)
        params = dict(
                      device_info = device_info,
                      fee_type = fee_type,
                      trade_type = trade_type,
                      product_id = product_id,
                      openid = openid,
                      spbill_create_ip = self.request.headers.get('X-Real-IP'),
                      
                      )
        order = order_serv.get_order_orderno(order_no)
        wait_pay_status = order_serv.order_status_description.index(u'待支付')
        expired_status = order_serv.order_status_description.index(u'已过期')
        if user_id != None and order.user_id != user_id:
            raise AppError("权限错误")
        if order.status != wait_pay_status and order.status != expired_status: #订单为未支付状态
            raise AppError(u"订单不支持支付操作")
        rep = wxpay.sign(params, order)
        log.debug(rep)
        if signOnServer is not None:
            return_code = rep.get('return_code')
            if return_code.lower() != 'success':
                return False
            result_code = rep.get('result_code')
            if result_code.lower() != 'success':
                return False
            sign = ''
            if rep.has_key('sign'):
                sign = rep.pop('sign')
                
            #过滤空值、sign与sign_type参数
            rep = wxpay.para_filter(rep)
            #获取待签名字符串
            pre_sign_str = wxpay.create_link_string(rep)
            #获得签名验证结果
            is_sign = wxpay.verify(pre_sign_str, sign)
            if is_sign:
                if rep.has_key('return_code'):
                    rep.pop('return_code')
                if rep.has_key('return_msg'):
                    rep.pop('return_msg')
                if rep.has_key('result_code'):
                    rep.pop('result_code')
                if rep.has_key('trade_type'):
                    rep.pop('trade_type')
                if rep.has_key('mch_id'):
                    rep.pop('mch_id')
                if rep.has_key('nonce_str'):
                    rep['noncestr'] = rep.pop('nonce_str')
                if rep.has_key('prepay_id'):
                    rep['prepayid'] = rep.pop('prepay_id')
#                 rep.pop('sign')
                rep = wxpay.prepare(rep)
                
        self.render_json(rep)

