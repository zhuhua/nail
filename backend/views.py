'''
Created on 2014-12-24

@author: zhuhua
'''
from simpletor import application

@application.RequestMapping("/manage")
class Login(application.RequestHandler):
    
    def get(self):
        self.render('artistan/artist.html')