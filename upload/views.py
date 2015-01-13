'''
Created on Jan 13, 2015

@author: zhuhua
'''
from simpletor import application
import settings

@application.RequestMapping("/upload_image")
class UploadAvatar(application.RequestHandler):
    
    def get(self, artisan_id):
        self.render('artisan/upload_avatar.html')
        
    def post(self):
        file_dict_list = self.request.files['file']
        filename = ''
        for file_dict in file_dict_list:
            filename = file_dict["filename"]
            f = open("%s/%s" % (settings.img_dir, filename), "wb")
            f.write(file_dict["body"])
            f.close()
        self.write("/img/%s" % filename)