# -*- coding:utf-8 -*-
'''
Created on 2014年12月18日

@author: zhuhua
'''
import os
import json
import hashlib
from io import BytesIO
from PIL import Image
import cStringIO
import base64
import settings

from datetime import date, datetime

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
        
def sha1pass(password):
    '''Password Hash'''
    sha1 = hashlib.sha1()
    sha1.update(password)
    return sha1.hexdigest()

def resizeImage(info, data, sizes):
    '''缩放图片'''
    data_io = BytesIO(base64.b64decode(data))
    md5 = hashlib.md5()
    md5.update(data_io.read())
    name = md5.hexdigest()
    data_io.seek(0)

    img = Image.open(data_io)
    fmt = info.split("/")[1]
    w, h = img.size
    
    images = []
    for width, height in sizes:
        
        img_new = None
        if w > width and w > h:
            new_w = width
            new_h = int(float(width) / w * h)
            img_new = img.resize((new_w, new_h), Image.ANTIALIAS)
        elif h > height and w < h:
            new_w = int(float(height) * w / h)
            new_h = height
            img_new = img.resize((new_w, new_h), Image.ANTIALIAS)
        else:
            img_new = img.resize((w, h), Image.ANTIALIAS)

        output = cStringIO.StringIO()
        img_new.save(output, fmt.upper(), quality = 95)
        img_data = output.getvalue()
        output.close()
        images.append(img_data)
        del img_new
        
    del img
    return name, fmt, images

def save_image(info, data, sizes=[(260, 170), (595, 375)]):
    '''保存图片到本地'''
    name, fmt, images = resizeImage(info, data, sizes)
    
    save_path = "%s/%s.%s" % (settings.img_dir, name, fmt)
    if os.path.isfile(save_path):
        return '%s.%s' % (name, fmt)
    
    i = 0
    for image in images:
        save_path = ""
        if i == 0:
            save_path = "%s/%s_s.%s" % (settings.img_dir, name, fmt)
        else:
            save_path = "%s/%s.%s" % (settings.img_dir, name, fmt)
        
        image_file = open(save_path, 'wb')
        image_file.write(image)
        image_file.close()
        i += 1

    return '%s.%s' % (name, fmt)

def get_image(img_name, thumb=False):
    if thumb:
        ext = img_name[img_name.rfind('.'):]
        img_name = img_name.replace(ext, "_s.%s" % ext[1:])
    return "/img/%s" % img_name
