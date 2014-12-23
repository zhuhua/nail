'''
Created on 2014-12-23

@author: zhuhua
'''
import unittest
import requests

prefix = 'http://127.0.0.1:8888%s'

class Test(unittest.TestCase):

    def testRegister(self):
        requests.post(prefix % '/register', data=dict(mobile='13812345678', password='123456'))


if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testRegister']
    unittest.main()