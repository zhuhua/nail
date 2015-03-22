'''
Created on 2015-1-25

@author: Zhuhua
'''
import json
import models
import services
from common import services as common_serv
from simpletor.torndb import transactional
from simpletor.utils import JSONEncoder
@transactional
def add_sample_image():
    obj_id = 28
    obj_type = 'sample'
    url = '/img/44af80ee7c225cef047e8b43191c31f3.jpg'
    common_serv.add_to_gallery(obj_id, obj_type, url)
# add_sample_image()
def test_get_gallery():
    obj_id = 28
    obj_type = 'sample'
    images = common_serv.get_gallery(obj_id, obj_type)
    
    return images

def test_upate():
    sample_id = 31
    s = services.get_sample(sample_id)
    services.update_sample(s)
# test_upate()

def test_get_sampel():
    sample_id = 31
    s = services.get_sample(sample_id)
    s.images =test_get_gallery()
    print json.dumps(s, cls = JSONEncoder)
test_get_sampel()
    
test_get_gallery()
if __name__ == '__main__':
#     items = models.sampleDAO.all()
    
#     for item in items:
#         sample = services.get_sample(item.id)
#         sample.tags = ' '.join(sample.tags)
#         try:
#             services.update_sample(sample)
#         except Exception, e:
#             print e
#     add_sample_image()
    print 'finish'