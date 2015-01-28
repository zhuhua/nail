# -*- coding:utf-8 -*-
'''
Created on Jan 28, 2015

@author: lisong
'''
from simpletor.torndb import transactional
from simpletor.application import AppError
from simpletor.tornsolr import index, connect
from simpletor.utils import validate_utils
from common import services as common_serv
import models
import settings

def appointment(artisan_id):
    for x in range(settings.appointmentRange[0], settings.appointmentRange[1] + 1):
        pass

@transactional
def close_appointment(artisan_id, appt_date, appt_hour):
    if appt_hour < settings.appointmentRange[0] or appt_hour > settings.appointmentRange[1]:
        raise AppError("超出可预约时间范围")
    appt = models.Appointment()
    appt.artisan_id = artisan_id
    appt.appt_date = appt_date
    appt.appt_hour = appt_hour
    
    models.appointmentDAO.save(**appt)