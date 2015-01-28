'''
tests.py
'''
import models
import services
import datetime

def test_closeAppointment():
    artisan_id = 28000009
    appt_date = datetime.date.today()
    appt_hour = 21
    services.close_appointment(artisan_id, appt_date, appt_hour)
    
def test_findAppointment():
    artisan_id = 28000009
    appt_date = datetime.date.today()
    items = models.appointmentDAO.find(artisan_id, appt_date)
    print items
    
test_findAppointment()
if __name__ == '__main__':
#     print datetime.date.today()
#     test_closeAppointment()
    pass