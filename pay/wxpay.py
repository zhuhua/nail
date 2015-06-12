# -*- coding:utf-8 -*-
'''
Created on 2015-03-13

@author: lisong
'''
import requests
import uuid
import md5
import time
import ConfigParser
from numbers import Number
import xml.etree.ElementTree as ET

from trade import services as trade_serv
from simpletor.application import AppError
from simpletor.utils import validate_utils
import logging

log = logging.getLogger(__name__)

class Wxpay:
    
    prepay_url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    
    notify_url = 'http://www.mecatmeizhuang.com/f/'
    
    def __init__(self):
        file_path = '/data/certs/wxpay.properties'
        try:
            config = ConfigParser.RawConfigParser()
            config.read(file_path)
            self.appid = config.get('Section1', 'appid')
            self.mch_id = config.get('Section1', 'mch_id')
            self.key = config.get('Section1', 'key')
        except:
            log.error('load wxpay.properties failed')
        
    def sign(self, client_params, order):
        
            
        if int(order.status) == trade_serv.order_status_description.index(u'已支付'):
            raise AppError(u'订单已经支付')
        params = dict(
                      appid = self.appid,
                      mch_id = self.mch_id,
                      nonce_str = self.generate_nonce_str(),#随机字符串
                      body = order.title, #商品或支付单简要描述 String(32)
                      detail = '', ###商品名称明细列表 String(8192)  
                      attach = '', ###附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据 String(127)  
                      out_trade_no = order.trade_no, #商户系统内部的订单号,32个字符内、可包含字母 String(32)
                      fee_type = 'CNY',  ##0#符合ISO 4217标准的三位字母代码，默认人民币：CNY 
                      total_fee = int(float(order.price) * 100),  #订单总金额，只能为整数 单位 分
                      time_start = None,  ###订单生成时间，格式为yyyyMMddHHmmss，如2009年12月25日9点10分10秒表示为20091225091010  
                      time_expire = None,  ###订单失效时间，格式为yyyyMMddHHmmss，如2009年12月27日9点10分10秒表示为20091227091010
                      goods_tag = None,  ###商品标记，代金券或立减优惠功能的参数
                      notify_url = self.notify_url,  #接收微信支付异步通知回调地址
                      trade_type = 'APP',#取值如下：JSAPI，NATIVE，APP
                      product_id = None, ###trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义。
                      openid = None,###trade_type=JSAPI，此参数必传，用户在商户appid下的唯一标识
                      )
        
        params.update(client_params)
#         params
        params = self.para_filter(params)
        logging.debug(params)
        stringA = self.create_link_string(params)
        
        sign = self.generate_sign(stringA)
        params['sign'] =  sign
        data = self.dump_xml(params)
        logging.debug(data)
        
        rep = requests.post(self.prepay_url, data=data)

        return self.parse_xml(rep.content)
    
    def generate_sign(self, stringA):
        stringSignTemp="%s&key=%s" % (stringA, self.key)
        m = md5.new()
        m.update(stringSignTemp)
        sign = m.hexdigest().upper()
        
        return sign
    
    def verify(self, content, sign):
        res = False
        try:
            signn = self.generate_sign(content)
            
            res = signn == sign.upper()
        except Exception, e:
            log.error(e)
            
        return res
    
    def para_filter(self, params):
        '''
        过虑值为空的参数及sign, sigh_type
        '''
        result = dict()
        if params is None or len(params) <= 0:
            return result
        
        for k, v in params.iteritems():
            if k.lower() == 'sign' or k.lower() == 'sign_type' or v is None or validate_utils.is_empty_str(v):
                continue
            if isinstance(v, unicode):
                v = v.encode('utf-8')
            result[k] = v
            
        return result
    
    def create_link_string(self, params):
        '''
        对参数按照key=value的格式，并按照参数名ASCII字典序排序
        '''
        keys = params.keys()
        keys.sort()
        
        param_str = ''
        for key in keys:
            param_str += '%s=%s&' % (key, params[key])

        length = len(param_str)
        if length > 1:
            return param_str[:len(param_str) - 1]
        
        return param_str
    
    def dump_xml(self, params):
        '''
        将字典转为xml
        '''
        root = ET.Element('xml')
        for k, v in params.iteritems():
            if v is not None:
#                 print type(v), v, k
                if isinstance(v, str):
                    v = v.decode('utf-8')
                if isinstance(v, Number):
                    v = unicode(str(v), 'utf-8');
                ET.SubElement(root, k).text = v
             
        return ET.tostring(root, encoding='utf-8')
    
    def parse_xml(self, content):
        '''
        解析xml返回字典
        '''
        root = ET.fromstring(content)
        params = dict()
        for c in root:
            if isinstance(c.text, unicode):
                params[c.tag] = c.text.encode("utf-8")
            else:
                params[c.tag] = c.text
        
        return params
    
    def generate_nonce_str(self):
        '''
        随机字符串
        '''
        return uuid.uuid4().hex
    
    def prepare(self, param):
        param['appid'] = self.appid
        param['partnerid'] = self.mch_id
        param['package'] = 'Sign=WXPay'
        param['timestamp'] = int(time.time())
        param['noncestr'] = self.generate_nonce_str()
        param = self.para_filter(param)
        logging.debug(param)
        stringA = self.create_link_string(param)
        
        sign = self.generate_sign(stringA)
        param['sign'] =  sign
        
        return param
wxpay = Wxpay()