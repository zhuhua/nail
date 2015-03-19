'''
tests.py
'''
import models
import services
import datetime
from simpletor import utils
from common import services as common_serv
from simpletor.torndb import transactional
from trade import services as trade_serv

def test_closeAppointment():
    artisan_id = 28000009
    appt_date = datetime.date.today()
    appt_hours = 21
    services.close_appointment(artisan_id, appt_date, appt_hours)
    
# test_closeAppointment()
    
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
# test_generate_random()

@transactional
def add_image():
    for obj_id in range(28, 32):
        obj_id = obj_id
        obj_type = 'sample'
        url = '/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg'
        common_serv.add_to_gallery(obj_id, obj_type, url);
# add_image()
@transactional
def test_trade():
    orders = (
             (5,1425868441183706),
            (5,1425868769944082),
            (5,1425872309250128),
            (5,1425873383688302),
            (3,1425885982887170),
            (3,1425886372246123),
            (5,1425910631800164),
            (3,1425914707085536),
            (3,1425914744823651),
            (3,1426053613660599),
            (3,1426172988125275),
            (3,1426173328193383),
            (5,1426173902110362),
            (5,1426174935661229),
            (3,1426175114178711),
            (3,1426175408165573),
            (6,1426233043347716),
            (6,1426241084750584),
            (6,1426242269601959),
            (6,1426244457237380),
            (6,1426244759260605),
            (3,1426300216906828),
            (3,1426602501195753),
            (6,1426660322411057),
            (6,1426663321821317),
            (6,1426663760915074),
            (6,1426664166943722),
            (6,1426664219057431),
            (6,1426664636748562),
            (6,1426664816481965),
            (6,1426664883510550),
            (6,1426669029768595),
            (6,1426669727855570),
            (6,1426670038276656),
            (6,1426670160729619),
            (6,1426670188328711),
            (8,1426688705828906),
              )
    for o in orders:
        print o[1]
        order = trade_serv.trade(o[0], str(o[1]), 'pay')
        print order.status
        
test_trade()

if __name__ == '__main__':
#     print datetime.date.today()
#     test_closeAppointment()
    pass