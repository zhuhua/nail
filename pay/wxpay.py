# -*- coding:utf-8 -*-
'''
Created on 2015-03-13

@author: lisong
'''
import requests
import json
import uuid
import md5
import ConfigParser

from trade import services as trade_serv
import xml.etree.ElementTree as ET

class Wxpay:
    
    prepay_url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    
    notify_url = ''
    
    def __init__(self):
        file_path = '/data/certs/wxpay.properties'
        
        config = ConfigParser.RawConfigParser()
        config.read(file_path)
        self.appid = config.get('Section1', 'appid')
        self.mch_id = config.get('Section1', 'mch_id')
        self.key = config.get('Section1', 'key')
        
    def sign(self, client_params):
        order_no = client_params.get('order_no')
        order = trade_serv.get_order_orderno(order_no)
        params = dict(
                      appid = self.appid,
                      mch_id = self.mch_id,
                      nonce_str = self.generate_nonce_str(),#随机字符串
                      body = order.title, #商品或支付单简要描述 String(32)
                      detail = '', ###商品名称明细列表 String(8192)  
                      attach = '', ###附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据 String(127)  
                      out_trade_no = order_no, #商户系统内部的订单号,32个字符内、可包含字母 String(32)
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
        self.para_filter(params)
        stringA = self.create_link_string(params)
        stringSignTemp="%s&key=%s" % (stringA, self.key)
        m = md5.new()
        m.update(stringSignTemp)
        sign=m.digest().upper()

    
        params['sign'] =  sign
        
        self.doRequest(self.prepay_url, params, 'get', self.xx)

    def verify(self, content, sign):
        res = False
        try:
            stringSignTemp="%s&key=%s" % (content, self.key)
            m = md5.new()
            m.update(stringSignTemp)
            signn=m.hexdigest().upper()
            
            res = signn == sign.upper()
        except Exception, e:
            print e
            
        return res
    
    def xx (self, data) :
        print 'Data :' 
        print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    
    def doRequest(self, url, params, method, dataHandler, token=''):
        '''
        Parameters:
            url  - 请求url
            params - 请求参数
            method - 请求方式 GET/POST
            dataHandler - 处理返回结果的方法
            token - 如果接口需要token则传入，如果不需要则不传
        '''
        headers = dict()
        if len(token) > 0:
            headers['Authorization']='%s' % token
        rep = None
        print headers
        if (method.lower() == 'get') :
            rep = requests.get(url, params=params,headers=headers)
        elif method.lower() == 'post' :
            rep = requests.post(url, data=params,headers=headers)
        print rep.url
        
        if rep.status_code == 200:
            dataHandler(rep.json())
        else :
            print "HTTP STATUS CODE: %s" % rep.status_code
            print rep.content
            
    def para_filter(self, params):
        '''
        过虑值为空的参数及sign, sigh_type
        '''
        result = dict()
        if params is None or len(params) <= 0:
            return result
        
        for k, v in params.iteritems():
            if k.lower() == 'sign' or k.lower() == 'sign_type':
                continue
                
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
        for k, v in params:
            ET.SubElement(root, k).text = v
             
        return ET.dump(root)
    
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
    
wxpay = Wxpay()