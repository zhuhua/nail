'''
Created on 2015-1-25

@author: Zhuhua
'''
import models
import services


if __name__ == '__main__':
    items = models.artisanDAO.all()
    
    for item in items:
        sample = services.get_artisan(item.id)
        services.update_profile(sample)