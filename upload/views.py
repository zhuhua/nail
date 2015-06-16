'''
Created on Jan 13, 2015

@author: zhuhua
'''
from simpletor import application
from simpletor import utils

@application.RequestMapping("/img/(.*)")
class Image(application.RequestHandler):
    
    def get(self, filename):
        ext, f = utils.get_image_file(filename)
        self.set_header("Content-Type", "image/%s" % ext.lower())
        self.write(f)

@application.RequestMapping("/upload_image")
class UploadAvatar(application.RequestHandler):

    def post(self):
        crop = self.get_argument("is_crop", default="true")
        
        is_crop = True
        if crop == 'false':
            is_crop = False
        
        file_dict_list = self.request.files['file']
        filename = ''
        for file_dict in file_dict_list:
            filename = file_dict["filename"]
            filename = utils.save_image(filename, file_dict["body"], is_crop=is_crop)
            
        data = dict(url="/img/%s" % filename)
        self.write(data)