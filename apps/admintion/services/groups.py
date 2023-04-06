from datetime import date
from django.db.models import OuterRef,Value,F,DateField,Q,Case,When,CharField
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import JSONObject,Concat,Cast
from django.contrib.postgres.expressions import ArraySubquery
from admintion.models import Group, FormLead,Student,Attendace
from admintion.utilts.users import get_days,get_month,get_attendace_days
from admintion.templatetags.custom_tags import attendance_result
from datetime import date,datetime

def get_attendace_data(id,educenter_ids,start_date,day_today):
    attendaces =Attendace.objects\
        .filter(group_student__student__id=OuterRef('pk'),date__gte=start_date,date__lte=day_today)\
        .annotate(
            reasen_title=Case(
                When(reasen=1,then=Value("Qattiq kasal bo'lgan")),
                When(reasen=2,then=Value('Talaba viloyatga ketgan')),
                When(reasen=3,then=Value("2-darsga kelmadi")),
                When(reasen=4,then=Value("3-darsga kelmadi")),
                default=None,
                output_field=CharField()
            )
        )\
        .values(
        attendaces=JSONObject(status='status', comment='comment',reasen='reasen_title',date='date',is_small=Value(True))
    ).values_list('attendaces')
    return Student.objects.filter(educenter__id__in=educenter_ids,ggroups__group__id=id).annotate(
            attendaces=ArraySubquery(attendaces),
            full_name = Concat(F('user__last_name'),Value(' '),F('user__first_name')),
            attendace=ArrayAgg(
                Cast('ggroups__attendance__date', DateField()),
                filter=Q(ggroups__attendance__date__isnull=False
            ))
        ).values('id','full_name','attendaces','attendace')

def get_attendace(id,start_date,educenter_ids,day_today=date.today(),group_days=[]):
    context = {}
    # print( Student.students.student_balances(id))
    context['students'] = Student.students.student_balances(id,educenter_ids)
    context['days'] = get_days(start_date,day_today,group_days)
    context['students_attendace'] = get_attendace_data(id,educenter_ids,min(context['days']),max(context['days']))
    # print(context['students_attendace'])
    # print(context['students_attendace'])
    # context['leads_attendace'] = FormLead.leads.leads_attendace(id)
    datas = []
    # context['leads_attendace'] = list(context['leads_attendace']) 
    # for lead in context['leads_attendace']:
    #     lead['enabled'] = lead['is_lead'] = True
    # context['students_attendace'] = list(context['students_attendace'])+context['leads_attendace']
    context['students_attendace'] = list(context['students_attendace'])
    if start_date is None:
        return context
    
    context['months'] = get_month(start_date,day_today)
    context['after_month'] = get_month(start_date,day_today)

    for count, val in enumerate([*context['students_attendace']]):
        datas.append(val)
        for index,item in enumerate(context['days']):
            if type(item)==str:
                item=datetime.strptime(item, '%Y-%m-%d').date()
            if item not in val['attendace']:
                datas[count]['attendaces'].append({
                            'date':item,
                            'status':0,
                            'reasen':None,
                            'comment':None,
                            'is_small':True if datetime.now().date()>=item else False
                        })
        vam = datas[count]['attendaces']
        vam.sort(key = lambda x: datetime.strptime(str(x['date']), '%Y-%m-%d'))
        datas[count]['attendaces']=vam
        # print(vam)
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


