# -*- coding:utf-8 -*-
'''
Created on 2015-1-11

@author: Zhuhua
'''
from simpletor.torndb import Transactional

import models

@Transactional()
def register(name, password, **profile):
    artist = models.Artist()
    artist.name = name
    artist.password = password
    artist.gender = profile.pop('gender', 1)
    
    avatar = profile.pop('avatar')
    brief = profile.pop('brief')
    
    if avatar:
        artist.avatar = avatar
    if brief:
        artist.brief = brief
        
    models.artistDAO.save(artist)
    
def get(artist_id):
    return models.artistDAO.find(artist_id)
    
@Transactional()
def update_profile(artist_id, **profile):
    artist = models.artistDAO.find(artist_id)
    if not artist:
        return
    
    name = profile.pop('gender', None)
    gender = profile.pop('gender', 1)
    avatar = profile.pop('avatar', None)
    brief = profile.pop('brief', None)
    
    if name:
        artist.name = brief
    if gender:
        artist.gender = gender
    if avatar:
        artist.avatar = avatar
    if brief:
        artist.brief = brief
    
    models.artistDAO.update(artist)
    