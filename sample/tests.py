'''
Created on 2015-1-25

@author: Zhuhua
'''
import models
import services


if __name__ == '__main__':
    items = models.sampleDAO.all()
    
    for item in items:
        sample = services.get_sample(item.id)
        sample.tags = ' '.join(sample.tags)
        try:
            services.update_sample(sample)
        except Exception, e:
            print e
    