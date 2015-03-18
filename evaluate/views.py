# -*- coding:utf-8 -*-
'''
Created on 2015-02-09

@author: lisong
'''
from simpletor import application
from simpletor.utils import save_image
from api import Api
from evaluate import models as evaluate_models
from evaluate import services as evaluate_serv

@application.RequestMapping("/api/evaluate/add")
class Add(application.RequestHandler):
    @Api(auth=True)
    def post(self):
        evaluate = evaluate_models.Evaluate()
        evaluate.author_id = self.user_id
        evaluate.communication_rank = self.get_argument('communication_rank', strip=True)
        evaluate.content = self.get_argument('content', strip=True)
#         evaluate.images = self.get_arguments('image', strip=True)
        evaluate.object_id = self.get_argument('object_id', strip=True)
        evaluate.object_type = self.get_argument('object_type', default = 'sample', strip=True)
        evaluate.professional_rank = self.get_argument('professional_rank', strip=True)
        evaluate.punctual_rank = self.get_argument('punctual_rank', strip=True)
        evaluate.rating = self.get_argument('rating', strip=True)
        evaluate.order_no = self.get_argument('order_no', strip=True)
        file_dict_list = self.request.files.get('file')
        filenames = list()
        for file_dict in file_dict_list:
            filename = file_dict["filename"]
            filename = save_image(filename, file_dict["body"])
            filenames.append('/img/%s' % filename)
            
        evaluate.images = filenames
        evaluate = evaluate_serv.add_evaluate(evaluate)

        self.render_json(evaluate)
        
@application.RequestMapping("/api/evaluates")
class GetEvaluates(application.RequestHandler):
    @Api()
    def get(self):
        sample_id = self.get_argument('sample_id', strip=True)
        rating = self.get_argument('rating', default = None, strip=True)
        page = self.get_argument('page', default = 1, strip=True)
        page_size = self.get_argument('page_size', default = 10, strip=True)
        evaluates, hits = evaluate_serv.get_evaluates(sample_id, rating, page, page_size)
        print hits
        counts = evaluate_serv.count_evaluates(sample_id)
        counts.update(dict(evaluates=evaluates))
        self.render_json(counts)