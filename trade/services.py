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
import datetime

def appointment_status(artisan_id, appt_date):
    if appt_date < datetime.date.today():
        raise AppError("超出可预约时间范围")
    appts = models.appointmentDAO.find(artisan_id, appt_date);
    appt_hours = list()
    appt_status = dict()
    appt_status['artisan_id'] = artisan_id
    appt_status['appt_date'] = appt_date
    for a in appts:
        appt_hours.append(a.appt_hour)
    for x in range(settings.appointmentRange[0], settings.appointmentRange[1] + 1):
        status = True
        if x in appt_hours:
            status = False
        appt_status[x] = status

    return appt_status

@transactional
def close_appointment(artisan_id, appt_date, appt_hour):
    if appt_hour < settings.appointmentRange[0] or appt_hour > settings.appointmentRange[1]:
        raise AppError("超出可预约时间范围")
    appt = models.Appointment()
    appt.artisan_id = artisan_id
    appt.appt_date = appt_date
    appt.appt_hour = appt_hour
    
    models.appointmentDAO.save(**appt)