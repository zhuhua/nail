# -*- coding:utf-8 -*-
'''
Created on Mar 3, 2015

@author: zhuhua
'''
import base64
import requests
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import logging

sign_type = 'RSA'

partner = ''
# 商户的私钥
private_key = '/data/certs/rsa_private_key.pem'
# 支付宝的公钥，无需修改该值
public_key = '/data/certs/rsa_public_key.pem'
 
class Alipay:
    
    HTTPS_VERIFY_URL = "https://mapi.alipay.com/gateway.do?service=notify_verify&partner=%s&notify_id=%s"
    
    def __init__(self):
        try:
            self.public_key = RSA.importKey(open(public_key,'r').read()) 
            self.private_key = RSA.importKey(open(private_key,'r').read())
        except Exception, e:
            logging.log('info', 'load pem file failed!')
            pass
    
    def sign(self, content):
        try:
            signer = PKCS1_v1_5.new(self.private_key)
            signed = signer.sign(SHA.new(content))
            signed = base64.b64encode(signed)
            return signed
        except Exception, e:
            print e
            return None

    def verify(self, content, sign):
        try:
            signn = base64.b64decode(sign)
            verifier = PKCS1_v1_5.new(self.public_key) 
            if verifier.verify(SHA.new(content), signn): 
                return True
        except Exception, e:
            print e
        return False
    
    def para_filter(self, params):
        result = dict()
        if params is None or len(params) <= 0:
            return result
        
        for k, v in params.iteritems():
            if k.lower() == 'sign' or k.lower() == 'sign_type':
                continue
            
            value = ','.join(v)
            if len(value.replace(',', '')) <= 0:
                continue
                
            result[k] = value
            
        return result

    def create_link_string(self, params):
        keys = params.keys()
        keys.sort()
        
        param_str = ''
        for key in keys:
            param_str += '%s=%s&' % (key, params[key])

        length = len(param_str)
        if length > 1:
            return param_str[:len(param_str) - 1]
        
        return param_str
    
    def verify_response(self, notify_id):
        veryfy_url = self.HTTPS_VERIFY_URL % (partner, notify_id)
        result = requests.get(veryfy_url)
        return result.content
    
alipay = Alipay()
    
