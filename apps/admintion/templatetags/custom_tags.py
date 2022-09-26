from django import template

from admintion.models import Attendace


register = template.Library()

def take_attendance_status(value,day):
    context = {
        '1':'Bor edi',
        '2':'Yoq',
        '3':'Kechikdi'
    }  
    status = Attendace.objects.filter(student__id=value,date=day).first().status
    return context[str(status)]

def attendance_result(value):
    attendace = Attendace.objects.filter(student__id=value)
    count=0
    if attendace.exists():
        goal = attendace.filter(status=1)
        count = goal.count()/attendace.count()
    return int(count*100)

def readable_soums(value):
    if value is None:
        return '0'
    res: str = ''
    counter = 0
    while value:
        r = value % 10
        value = value // 10
        res = str(r) + res
        counter += 1
        if counter == 3 and value != 0:
            res = " " + res
            counter = 0
    return res

def get_status(value):
    status = "success"
    if value == 2:
        status = "warning"
    elif value == 3:
        status = "danger"
    return status

def get_status_name(value):
    status = "active"
    if value == 2:
        status = "deactivated"
    elif value == 3:
        status = "removed"
    return status

register.filter('take_attendance_status', take_attendance_status) 
register.filter('attendance_result', attendance_result) 
register.filter('readable_soums', readable_soums)
register.filter('get_status', get_status)
register.filter('get_status_name', get_status_name)