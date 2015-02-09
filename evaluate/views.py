# -*- coding:utf-8 -*-
'''
Created on 2015-02-09

@author: lisong
'''
from simpletor import application
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
        evaluate.images = self.get_argument('image', strip=True)
        evaluate.object_id = self.get_argument('object_id', strip=True)
        evaluate.object_type = self.get_argument('object_type', default = 'order', strip=True)
        evaluate.professional_rank = self.get_argument('professional_rank', strip=True)
        evaluate.punctual_rank = self.get_argument('punctual_rank', strip=True)
        evaluate.rating = self.get_argument('rating', strip=True)
        
        evaluate_serv.add_evaluate(evaluate)
