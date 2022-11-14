from django import template
from django.shortcuts import get_object_or_404

import datetime
from admintion.models import Attendace, GroupStudents, LeadDemo,LeadForms
from ..data import chooses
from user.data import chooses as user_chooses
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
    gr_student_ids = [_.id for _ in GroupStudents.objects.filter(student_id=value)]
    attendace = Attendace.objects.filter(group_student_id__in=gr_student_ids)
    count=0
    if attendace.exists():
        goal = attendace.filter(status=1)
        count = goal.count()/attendace.count()
    return int(count*100)

def lead_attendance_result(value):
    gr_student_ids = [_.id for _ in LeadDemo.objects.filter(lead_id=value)]
    attendace = Attendace.objects.filter(lead_demo_id__in=gr_student_ids)
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

def get_status2(value):
    status = "info"
    if value == 2:
        status = "success"
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

def get_type_name(value, arg):
    if value ==None:
        return ''

    if arg == 'task':
        return dict(chooses.TASK_STATUS)[value] or ""
    if arg == "source":
        return dict(chooses.STUDENT_SOURCES)[value] or ""
    elif arg == "status":
        return dict(chooses.STUDENT_STATUS)[value] or ""
    elif arg == "gender":
        return dict(user_chooses.COURSES_SEXES)[value] or ""
    elif arg == "day":
        return dict(chooses.GROUPS_DAYS)[value] or ""
    elif arg == "attendance":
        return dict(chooses.STUDENT_ATTANDENCE_TYPE)[value] or ""
    elif arg == "payment":
        return dict(chooses.PAYMENT_TYPE)[value] or ""
    return value

def readable_days(value):
    result: str = ''
    if type(value) == int:
        value = get_object_or_404(GroupStudents, pk=value).group
    for day in value.days.all():
        try:
            result += str(dict(chooses.GROUPS_DAYS)[day.days]) + "/"
        except:
            pass
    if result[-1] == "/":
        return result[:-1]
    return result

def readable_days2(values): # values GroupDays modelining obyektlari
    result: str = ''
    for value in values:
        result+=str(dict(chooses.GROUPS_DAYS)[value.days])+ "/"
    return result

def readable_days3(values): # values -> hafta kunining raqami.
    result: str = ''
    for value in values:
        result+=str(dict(chooses.GROUPS_DAYS)[int(value)])+ "/"
    return result

def get_week_day(value):
    if value is None or type(value) != datetime.date:
        return ''
    day = value.weekday()
    return dict(chooses.GET_GROUPS_DAYS)[day+1] or ''

def get_conversion(id):
    leadform = LeadForms.objects.filter(id=id).first()
    if leadform:
        try:
            return leadform.seen/(leadform.formlead_set.all())
        except:
            return 0
    return 0


def get_conversion_status(id):
    leadform = LeadForms.objects.filter(id=id).first()
    if leadform:
        try:
            per = leadform.seen/(leadform.formlead_set.all())
        except:
            per = 0  
        if per >= 90:
            return 'success'
        elif per >= 70:
            return 'warning'
        else:
            return 'danger'



register.filter('take_attendance_status', take_attendance_status) 
register.filter('attendance_result', attendance_result) 
register.filter('readable_soums', readable_soums)
register.filter('get_status', get_status)
register.filter('get_status_name', get_status_name)
register.filter('get_type_name', get_type_name)
register.filter('readable_days', readable_days)
register.filter('readable_days2', readable_days2)
register.filter('readable_days3', readable_days3)
register.filter('get_week_day', get_week_day)
register.filter('get_status2', get_status2)
register.filter('lead_attendance_result', lead_attendance_result) 
register.filter('get_conversion', get_conversion)
register.filter('get_conversion_status', get_conversion_status)