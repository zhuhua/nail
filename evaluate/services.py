# -*- coding:utf-8 -*-
'''
Created on Feb 9, 2015

@author: lisong
'''
from datetime import datetime
from simpletor.torndb import transactional
from simpletor.application import AppError
from simpletor.utils import validate_utils, get_level
from simpletor.tornredis import cacheable, cacheevict

from evaluate import models
from common import services as common_services
from trade import services as trade_services
from artisan import services as artisan_services

evaluate_rating = ('好评', '中评', '差评')
evaluate_rank_range = (0, 1, 2, 3, 4, 5)
count_score = (1, 0, -1)
evaluate_expire_day = 30

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
    if evaluate.id is None and validate_utils.is_empty_str(evaluate.order_no):
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
    validate_evaluate(evaluate)
        
    order_no = evaluate.order_no
    object_id = evaluate.object_id
    
    order = trade_services.get_order_orderno(order_no)
    
    if long(order.sample_id) != long(object_id):
        raise AppError(u'评价样品错误')
    
    evaluate.author_mobile = order.telephone
    evaluate.author_avatar = order.buyer_avatar
    evaluate.object_name = order.sample_name
    
    evaluate_id = models.evaluateDAO.save(**evaluate)
    #保存评价图片
    images = evaluate.images
    save_images(images, evaluate_id)
    #修改订单评价状态
    order = trade_services.review(order_no, evaluate.author_id)
    
    # 新增评价或修改评价且评价级别发生变化 修改手艺人积分
    artisan_id = order.artisan_id
    change_score(artisan_id, evaluate, evaluate_id)
    
    evaluate = get_evaluate(evaluate_id)
    return evaluate

@transactional
@cacheevict('#evaluate.id', prefix='EVALUATE')
def edit_evaluate(evaluate):
    validate_evaluate(evaluate)
    o_evaluate = models.evaluateDAO.find(evaluate.id)
    if o_evaluate is None:
        raise AppError(u'评价不存在')
    
    if (datetime.now() - o_evaluate.create_time).days > evaluate_expire_day:
        raise AppError(u'评价不可修改')
    
    o_evaluate.rating = evaluate.rating
    o_evaluate.communication_rank = evaluate.communication_rank
    o_evaluate.professional_rank = evaluate.professional_rank
    o_evaluate.punctual_rank =evaluate.punctual_rank
    o_evaluate.update_time = datetime.now()
    evaluate_id = o_evaluate.id
    models.evaluateDAO.update(**o_evaluate)
    #保存评价图片
    common_services.remove_all(o_evaluate.id, 'evaluate')
    images = evaluate.images
    save_images(images, evaluate_id)
    
    # 新增评价或修改评价且评价级别发生变化 修改手艺人积分
    order_no = o_evaluate.order_no
    order = trade_services.get_order_orderno(order_no)
    artisan_id = order.artisan_id
    change_score(artisan_id, evaluate, evaluate_id)
    
    evaluate = get_evaluate(evaluate_id)
    return evaluate

@cacheable('#evaluate_id', prefix='EVALUATE')
def get_evaluate(evaluate_id):
    evaluate = models.evaluateDAO.find(evaluate_id)
    if evaluate == None:
        raise AppError(u'评价不存在')
    
    images = common_services.get_gallery(evaluate.id, 'evaluate')
    
    imgs = list()
    for image in images:
        imgs.append(image.url)
    evaluate['images'] = imgs
    
    return evaluate

def get_evaluates(sample_id, rating, page, page_size, object_type = 'sample'):
    
    page = int(page)
    page_size = int(page_size)
    first_result = (page - 1) * page_size
    
#     hits = models.evaluateDAO.count_obj_id(sample_id, object_type)
    evaluates_id = models.evaluateDAO.find_obj_id(sample_id, object_type, page_size, first_result)
    if rating != None:
#         hits = models.evaluateDAO.count_obj_id_rating(sample_id, rating, object_type)
        evaluates_id = models.evaluateDAO.find_obj_id_rating(sample_id, rating, object_type, page_size, first_result)
    evaluates = list()
    for eid in evaluates_id:
        try:
            evaluates.append(get_evaluate(eid.get('id')))
        except:
            print 'evaluate not exits (id:%s)' % eid
        
    return evaluates

def count_evaluates(sample_id, object_type = 'sample'):
    
    count_all = models.evaluateDAO.count_obj_id(sample_id, object_type)
    count_good = models.evaluateDAO.count_obj_id_rating(sample_id, 0, object_type)
    count_normal = models.evaluateDAO.count_obj_id_rating(sample_id, 1, object_type)
    count_bad = models.evaluateDAO.count_obj_id_rating(sample_id, 2, object_type)
    
    res = dict(total=count_all['total'], 
               good=count_good['total'], 
               normal=count_normal['total'],
               bad=count_bad['total'])
    
    return res
    
def count_rank(counts, evaluate):
        rank_keys = ('communication_rank', 'professional_rank', 'punctual_rank')
        for rk in rank_keys:
            xr = int(evaluate[rk]) * 10
            if counts.has_key(rk):
                xr = (int(counts[rk]) + xr) / 2
            counts[rk] = xr
            
def save_images(images, evaluate_id):
    for image in images:
        common_services.add_to_gallery(evaluate_id, 'evaluate', image)
        
def change_score(artisan_id, evaluate, evaluate_id, o_evaluate = None):
    artisan = artisan_services.get_artisan(artisan_id)
    score = 0
    counts = artisan.counts
    if counts.has_key('score'):
        score = artisan.counts['score']
        
    rating = int(evaluate.rating)
    
    if o_evaluate is not None:
#         评价级别发生变化 修改手艺人积分
        score += o_evaluate.rating - rating
    else:
        score += count_score[rating]
    artisan.counts['score'] = score
    artisan.level = get_level(score)
#     
    count_rank(artisan.counts, evaluate)
    
    artisan_services.update_profile(artisan)
    
    
    