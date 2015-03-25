'''
Created on 2015-1-25

@author: Zhuhua
'''
import models
import services


if __name__ == '__main__':
#     items = models.artisanDAO.all()
#     
#     for item in items:
#         sample = services.get_artisan(item.id)
#         services.update_profile(sample)
    user_id = 4
    page = 1
    page_size = 10
    order_by = 'create_time'
    sort = 'DESC'
    print services.my_artisan(user_id, page, page_size, order_by, sort)