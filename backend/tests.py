# -*- encoding: utf-8 -*-
'''
Created on 2015-03-24

@author: lisong
'''
import models
import services

def add_banner():
    banner = models.Banner()
    banner.name = 'banner-2'
    banner.cover = '/img/667b5b4a2addc4696602b498a73c0d04.jpg'
    detail = list()
    detail.append(dict(image='/img/243f6827fe80944b6bb26e80e175c713.jpg', description='00活动内容描述00', serial_number=0))
    detail.append(dict(image='/img/174509341416b35b7cf23cf41b04906c.jpg', description='11活动内容描述11', serial_number=1))
    banner.detail = detail
    banner.serial_number = 1
    banner.url = "http://photo.cankaoxiaoxi.com/roll10/2015/0324/717027_2.shtml"
    services.add_banner(banner)

def get_banners():
    print services.get_banners()
    
def get_banner():
    banner_id = 1
    print services.get_banner(banner_id)
if __name__ == '__main__':
#     add_banner()
#     get_banners()
    get_banner()
    pass