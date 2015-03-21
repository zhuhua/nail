'''
Created on 2015-1-25

@author: Zhuhua
'''
import models
import services
from common import services as common_serv
from simpletor.torndb import transactional

@transactional
def add_sample_image():
    obj_id = 28
    obj_type = 'sample'
    url = '/img/44af80ee7c225cef047e8b43191c31f3.jpg'
    common_serv.add_to_gallery(obj_id, obj_type, url)
    
def test_upate():
    sample_id = 31
    s = services.get_sample(sample_id)
    services.update_sample(s)

test_upate()
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