# -*- coding:utf-8 -*-
'''
Created on Feb 9, 2015

@author: lisong
'''
from simpletor.torndb import transactional
from simpletor.application import AppError
from simpletor.utils import validate_utils

from evaluate import models
from common import services as common_services
from trade import services as trade_services

evaluate_rating = ('好评', '中评', '差评')
evaluate_rank_range = (1,2,3,4,5)

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
    if not is_correct_rank(evaluate.communication_rank):
        raise AppError('评分超出范围', field='professional_rank')
    if not is_correct_rank(evaluate.communication_rank):
        raise AppError('评分超出范围', field='punctual_rank')
    if not is_correct_rank(evaluate.communication_rank):
        raise AppError('请填写发起评价的订单号', field='order_no')
    
    if validate_utils.is_empty_str(evaluate.content):
        raise AppError('请为手艺专业水平评分', field='professional_rank')
    if validate_utils.is_empty_str(evaluate.content):
        raise AppError('请为手艺守时情况评分', field='punctual_rank')
    if validate_utils.is_empty_str(evaluate.rating):
        raise AppError('请选择评价级别', field='rating')
    if not (int(evaluate.rating) in (0, 1, 2)):
        raise AppError('评价级别超出范围', field='rating')
    
    if len(evaluate.images) == 0:
        raise AppError('至少上传一张图片', field='image')

@transactional
def add_evaluate(evaluate):
    '''添加评价'''
    validate_evaluate(evaluate)
    images = evaluate.images
    order_no = evaluate.order_no
    order = trade_services.get_order_orderno(order_no)
    
    if order == None:
        raise AppError('订单不存在', field='order_no')
    if order.status != trade_services.order_status_description.index('已完成'):
        raise AppError('订单未成功不能评价', field='order_no')
    
    sample_id = models.evaluateDAO.save(**evaluate)
    for image in images:
        common_services.add_to_gallery(sample_id, 'evaluate', image)
        
def get_evaluates(sample_id, page, page_size, object_type = 'sample'):
    page = int(page)
    page_size = int(page_size)
    first_result = (page - 1) * page_size
    hits = models.evaluateDAO.count_obj_id(sample_id)
    evaluates = models.evaluateDAO.find_obj_id(sample_id, object_type, page_size, first_result)
    
    return evaluates, hits['total']