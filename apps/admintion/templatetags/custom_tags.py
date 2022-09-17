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
    
register.filter('take_attendance_status', take_attendance_status) 
register.filter('attendance_result', attendance_result) 
    
