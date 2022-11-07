from datetime import date

from admintion.models import Group, FormLead,Student
from admintion.utilts.users import get_days,get_month,get_attendace_days
from admintion.templatetags.custom_tags import attendance_result
from datetime import date,datetime

def get_attendace(id,start_date,day_today=date.today()):
    context = {}
    context['students'] = Student.students.student_balances(id)
    context['students_attendace'] = Student.students.students_attendace(id)
    context['leads_attendace'] = FormLead.leads.leads_attendace(id)
    context['days'] = get_days(start_date,day_today)
    context['months'] = get_month(start_date,day_today)
    context['after_month'] = get_month(start_date,day_today)
    datas = []
    context['leads_attendace'] = list(context['leads_attendace']) 
    for lead in context['leads_attendace']:
        lead['enabled'] = lead['is_lead'] = True
    context['students_attendace'] = list(context['students_attendace'])+context['leads_attendace']
    for count, value in enumerate(context['students_attendace']):
        datas.append(value)
        dats = []
        for index,item in enumerate(context['days']):
            check_true = False
            for key,val in enumerate(value['attendace']):
                time = datetime.strptime(f'{val}', "%Y-%m-%d")
                if type(item) == str:
                    item = datetime.strptime(f'{str(item)}', "%Y-%m-%d")
                if time == item:
                    check_true=True
                    dats.append({
                        'attendaces':value['attendace'][key],
                        'status':value['attendace_status'][key]
                    })
                    break
            if not check_true:
                dats.append({
                        'attendaces':item,
                        'status':0
                    })   
          
            datas[count]['attendaces'] =dats
    context['students_attendace']=datas
    return context

def get_days_attendace(id,start_date,day_today=date.today()):
    context = {}
    context['students_attendace'] = Student.students.students_attendace(id)
    context['days'] = get_days(start_date,day_today)
    datas = []
    for count, value in enumerate(context['students_attendace']):
        datas.append(value)
        dats = []
        for index,item in enumerate(context['days']):
            check_true = False
            for key,val in enumerate(value['attendace']):
                time = datetime.strptime(f'{val}', "%Y-%m-%d")
                if type(item) == str:
                    item = datetime.strptime(f'{str(item)}', "%Y-%m-%d")
                if time == item:
                    check_true=True
                    dats.append({
                        'attendaces':value['attendace'][key],
                        'status':value['attendace_status'][key]
                    })
                    break
            if not check_true:
                dats.append({
                        'attendaces':item,
                        'status':0
                    })   
          
            datas[count]['attendaces'] =dats
    context['students_attendace']=datas
    return context
