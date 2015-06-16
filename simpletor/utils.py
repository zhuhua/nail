# -*- coding:utf-8 -*-
'''
Created on 2014年12月18日

@author: zhuhua
'''
import os
import json
import hashlib
import cStringIO
import settings
import re
import random
import time

from PIL import Image
from io import BytesIO

from datetime import date, datetime
import application

class ValidateUtils:
    '''验证工具类'''
    def is_empty_str(self, string):
        if string is None or string == '':
            return True
        return False
    
    def is_mobile(self, string):
        return re.match('^1[3-8][0-9]\d{8}$', string)
    
    
    
validate_utils = ValidateUtils() 

class JSONEncoder(json.JSONEncoder):
    '''Json 编码器'''
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
        
def md5(source):
    '''MD5'''
    _md5 = hashlib.md5()
    _md5.update(source)
    return _md5.hexdigest()
        
def sha1(password):
    '''Password Hash'''
    _sha1 = hashlib.sha1()
    _sha1.update(password)
    return _sha1.hexdigest()


def crop(img, sizes):
    '''裁切'''
    fmt = img.format
    w, h = img.size
    aspect = w;
    x, y = 0, 0
    
    if w > h:
        aspect = h;
        x = (w - aspect) / 2;
    else:
        y = (h - aspect) / 2;
        
    img = img.crop((x, y, x + aspect, y + aspect))
    
    images = []
    for width, height in sizes:
        img_new = img.resize((width, height), Image.ANTIALIAS)
        output = cStringIO.StringIO()
        img_new.save(output, fmt, quality = 95)
        img_data = output.getvalue()
        output.close()
        images.append(img_data)
        del img_new
        
    del img
    return images

def save_image(filename, data, sizes=[(320, 320), (640, 640)], is_crop=False):
    '''保存图片到本地'''
    data_io = BytesIO(data)
    name = md5(data_io.read())
    ext = filename.split(".")[1]
    data_io.seek(0)
    
    img = Image.open(data_io)
    if is_crop:
        images = crop(img, sizes)
    else:
        images = [img]
    
    save_path = "%s/%s.%s" % (settings.img_dir, name, ext)
    if os.path.isfile(save_path):
        return '%s.%s' % (name, ext)
    
    i = 0
    for image in images:
        save_path = ""
        if i == 0:
            save_path = "%s/%s_s.%s" % (settings.img_dir, name, ext)
        else:
            save_path = "%s/%s.%s" % (settings.img_dir, name, ext)
        
        image_file = open(save_path, 'wb')
        image_file.write(image)
        image_file.close()
        i += 1

    return '%s.%s' % (name, ext)

def get_image(img_name, thumb=False):
    if thumb:
        ext = img_name[img_name.rfind('.'):]
        img_name = img_name.replace(ext, "_s.%s" % ext[1:])
    return "/img/%s" % img_name

def get_image_file(img_name, thumb=False):
    ext = img_name[img_name.rfind('.'):]
    if thumb:
        img_name = img_name.replace(ext, "_s.%s" % ext[1:])
        
    try:
        f = open("%s/%s" % (settings.img_dir, img_name), "rb")
        return ext, f.read()
    except:
        return ext, ''
    
def generate_order_no():
    return '%d' % (int(time.time() * 1000 * 1000))

def generate_random(start, end):
    return int(random.Random().random() * (end - start)) + start

def str2time(date_str, pattern = "%Y-%m-%d"):
    d = None
    try:
        d = time.strptime(date_str, pattern)
    except ValueError:
        raise application.AppError('日期转换出错')
    return d

def str2date(date_str, pattern = "%Y-%m-%d"):
    d = None
    try:
        d = datetime.strptime(date_str, pattern).date()
    except ValueError:
        raise application.AppError('日期转换出错')
    return d

def str2datetime(date_str, pattern = "%Y-%m-%d"):
    d = None
    try:
        d = datetime.strptime(date_str, pattern)
    except ValueError:
        raise application.AppError('日期转换出错')
    return d

def get_level(score):
    grade = 0
    if score > 0:
        scoreGrade = (0, 1, 2, 4, 9, 15, 31, 58, 94, 147, 211, 286, 385, 508, 656, 829, 1026, 1307, 1644, 2037, 2486, 2991, 3608, 4337, 5178, 6131,7196)
        grade = len(scoreGrade) - 1
        while grade > 0:
            if score >= scoreGrade[grade]:
                break
            grade -= 1
    
    return grade;