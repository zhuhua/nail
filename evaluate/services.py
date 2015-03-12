# -*- coding:utf-8 -*-
'''
Created on Feb 9, 2015

@author: lisong
'''
from simpletor.torndb import transactional
from simpletor.application import AppError
from simpletor.utils import validate_utils, get_level

from evaluate import models
from common import services as common_services
from trade import services as trade_services
from artisan import services as artisan_services

evaluate_rating = ('好评', '中评', '差评')
evaluate_rank_range = (0, 1,2,3,4,5)
count_score = (1, 0, -1)

def is_correct_rank(rank):
    if int(rank) in evaluate_rank_range:
        return True
    return False

def validate_evaluate(evaluate):
    if validate_utils.is_empty_str(evaluate.content):
        raise AppError('请填写评价内容', field='content')
    if validate_utils.is_empty_str(evaluate.communication_rank):
        raise AppError('请为手艺沟通能力评分', field='communication_rank')
    if not is_correct_rank(evaluate.communication_rank):
        raise AppError('评分超出范围', field='communication_rank')
    if validate_utils.is_empty_str(evaluate.professional_rank):
        raise AppError('请为专业能力评分', field='professional_rank')
    if not is_correct_rank(evaluate.professional_rank):
        raise AppError('评分超出范围', field='professional_rank')
    if validate_utils.is_empty_str(evaluate.professional_rank):
        raise AppError('请为守时情况评分', field='professional_rank')
    if not is_correct_rank(evaluate.punctual_rank):
        raise AppError('评分超出范围', field='punctual_rank')
    if validate_utils.is_empty_str(evaluate.order_no):
        raise AppError('请填写发起评价的订单号', field='order_no')
    
    if validate_utils.is_empty_str(evaluate.rating):
        raise AppError('请选择评价级别', field='rating')
    if not (int(evaluate.rating) in (0, 1, 2)):
        raise AppError('评价级别超出范围', field='rating')
    
    if len(evaluate.images) == 0:
        raise AppError('至少上传一张图片', field='image')

@transactional
def add_evaluate(evaluate):
    '''添加评价'''
    def count_rank(counts):
        rank_keys = ('communication_rank', 'professional_rank', 'punctual_rank')
        for rk in rank_keys:
            xr = int(evaluate[rk]) * 10
            if counts.has_key(rk):
                xr = (int(counts[rk]) + xr) / 2
            counts[rk] = xr
    validate_evaluate(evaluate)
    images = evaluate.images
    order_no = evaluate.order_no
    
    evaluate_id = models.evaluateDAO.save(**evaluate)
    for image in images:
        common_services.add_to_gallery(evaluate.object_id, 'evaluate', image)
    #修改订单评价状态
    order = trade_services.review(order_no, evaluate.author_id)
    #修改手艺人积分
    artisan_id = order.artisan_id
    artisan = artisan_services.get_artisan(artisan_id)
    score = 0
    counts = artisan.counts
    if counts.has_key('score'):
        score = artisan.counts['score']
    rating = int(evaluate.rating)
    score += count_score[rating]
    artisan.counts['score'] = score
    artisan.level = get_level(score)
#     
    count_rank(artisan.counts)
    
    artisan_services.update_profile(artisan)
    evaluate = models.evaluateDAO.find(evaluate_id)
    
    return evaluate

def get_evaluates(sample_id, page, page_size, object_type = 'sample'):
    page = int(page)
    page_size = int(page_size)
    first_result = (page - 1) * page_size
    hits = models.evaluateDAO.count_obj_id(sample_id, object_type)
    evaluates = models.evaluateDAO.find_obj_id(sample_id, object_type, page_size, first_result)
    
    return evaluates, hits['total']