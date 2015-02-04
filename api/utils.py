# -*- coding:utf-8 -*-
'''
Created on Feb 4, 2015

@author: zhuhua
'''
import requests
import random
from simpletor import tornredis
from xml.dom import minidom

def sendsms(mobile, content):
    data = dict(sname='dlsdcs00', spwd='zW46mgXE', scorpid='', sprdid='1012818', sdst=mobile, smsg=content)
    r = requests.post('http://cf.lmobile.cn/submitdata/Service.asmx/g_Submit', data)
    doc = minidom.parseString(r.content)
    state = int(doc.getElementsByTagName('State')[0].firstChild.data)
    
    if int(state) == 0:
        return True
    return False
    
class Checkcode:
    
    def generate(self):
        code, i = '', 0
        while i < 6:
            code += str(random.choice(range(10)))
            i += 1
        return code
    
    def key(self, mobile):
        return 'CHECKCODE_%s' % mobile
    
    def send(self, mobile):
        sms_template = u'您的验证码是：%s。请不要把验证码泄露给其他人。【百分信息】'
        code = self.generate()
        content = sms_template % code
        result = sendsms(mobile, content)
        if result:
            tornredis.connect.set(self.key(mobile), code)
            
    def validate(self, mobile, code):
        s_code = tornredis.connect.get(self.key(mobile))
        if s_code == code:
            tornredis.connect.delete(self.key(mobile))
            return True
        return False
        
checkcode = Checkcode()