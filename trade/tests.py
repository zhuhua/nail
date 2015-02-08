'''
tests.py
'''
import models
import services
import datetime
from simpletor import utils

def test_closeAppointment():
    artisan_id = 28000009
    appt_date = datetime.date.today()
    appt_hours = 21
    services.close_appointment(artisan_id, appt_date, appt_hours)
    
test_closeAppointment()
    
def test_findAppointment():
    artisan_id = 28000009
    appt_date = datetime.date.today()
    items = models.appointmentDAO.find(artisan_id, appt_date)
    print items
# test_findAppointment()
    
def test_appointment_status():
    artisan_id = 28000009
    appt_date = datetime.date.today()
#     appt_date = datetime.date(2015,1,29)
    print appt_date
    apptss = services.appointment_status(artisan_id, appt_date)
    
    print apptss
# test_appointment_status()

def test_generate_random():
    start = 1
    end = 100
    print utils.generate_random(start, end)
    
test_generate_random()

if __name__ == '__main__':
#     print datetime.date.today()
#     test_closeAppointment()
    pass