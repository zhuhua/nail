'''
Created on 2014-12-23

@author: zhuhua
'''
import unittest
import services


class Test(unittest.TestCase):

#     def testRegister(self):
#         mobile = '18583373989'
#         password = '123456'
#         user = services.register(mobile, password)
#         self.assertEqual(mobile, user.mobile)
         
    def testLogin(self):
        mobile = '18583373989'
        password = '123456'
        token = services.login(mobile, password)
        self.assertEqual(len(token.token), 32)


if __name__ == "__main__":
#     import sys;sys.argv = ['', 'Test.testRegister']
    unittest.main()