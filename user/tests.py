'''
Created on 2014-12-23

@author: zhuhua
'''
import unittest
import services
import models

class Test(unittest.TestCase):

#     def testRegister(self):
#         mobile = '18583373989'
#         password = '123456'
#         user = services.register(mobile, password)
#         self.assertEqual(mobile, user.mobile)
         
#     def testLogin(self):
#         mobile = '18583373989'
#         password = '123456'
#         token = services.login(mobile, password)
#         self.assertEqual(len(token.token), 32)


    def test_get_favorite_by_user(self):
        user_id = 3
        fav_type = '1'
        status = 0
        limit = 20
        offset = 0
        favs = models.favoriteDAO.find_by_user(user_id, fav_type, status, limit, offset)
        print favs
if __name__ == "__main__":
#     import sys;sys.argv = ['', 'Test.testRegister']
    unittest.main()