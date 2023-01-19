from admintion.models import GroupStudents,Group
from finance.models import StudentBalance,Paid,Jobs
from datetime import datetime,date
from django.db.models import Q
import calendar
from datetime import datetime,timedelta
import numpy as np
import time


def student_paid(student,price,paid_type,goal_type,description,user):
    paid = Paid(
            student=student,
            paid=price,
            paid_type=paid_type,
            description=description,
            user=user
        )
    title=None
    if goal_type!="0":
        group = Group.objects.filter(id=int(goal_type)).first() 
        paid.group=group
        paid.goal_type=3
        title=group.title
    else:
        title="Balans"
        paid.goal_type=1
    
    paid.save()
    if int(paid_type)<5:
        student_balance = StudentBalance.objects.filter(title=title,student=student).first()
        if student_balance is None:
            student_balance = StudentBalance.objects.create(title=title,student=student) 
        student_balance.balance=student_balance.balance+int(price)
        student_balance.save()
        paid.status=True
    return {
        'balance':student_balance.balance,
        'paid_id':paid.pk
    }

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return date(year, month, day)

def last_day_of_month(any_day):
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = any_day.replace(day=28) + timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return next_month - timedelta(days=next_month.day)

def cal_12days(day1,group_days,count_day,weekday_count=0):
    cal = calendar.Calendar()
    dat = {}
    for week in cal.monthdayscalendar(day1.year, day1.month):
        for i, day in enumerate(week):
            # not this month's day or a weekend
            # print(day1.day,day)
            # print(day1.day>day,day1.day,day)
            if day == 0 or (i+1 not in group_days or day1.day>day):
                continue
            if weekday_count==count_day:
                return dat
            weekday_count += 1
            dat['day']=day  
            dat['weekday_count']=weekday_count
    return dat       

def cal_days(day1,day2,group_days,bl_check=True):
    weekday_count = 0
    cal = calendar.Calendar()

    for week in cal.monthdayscalendar(day1.year, day1.month):
        for i, day in enumerate(week):
            # not this month's day or a weekend
            if day == 0 or (i+1 not in group_days):
                continue
            # or some other control if desired...
            if int(day1.day)<=day and bl_check:
                return weekday_count
            weekday_count += 1
    return weekday_count        

def find_last_lesson(day1,group_days):
    weekmask=[0]*7
    last_ls = cal_12days(day1,group_days,count_day=12)
    next_month = last_day_of_month(day1)
    if last_ls['weekday_count']!=12:
        next_month=add_months(day1,1).replace(day=1)
        last_ls=cal_12days(next_month,group_days,count_day=6)
    return next_month.replace(day=last_ls['day'])   

def count_lesson(start_date,group_days,end_date):
    weekmask=[0]*7
    for day in group_days:
       weekmask[day-1]=1  
    return np.busday_count(start_date,end_date,weekmask=weekmask)       
    

def pay_lesson(obj,end_lesson_date):
    dif_day = 12-count_lesson(obj['created'],end_lesson_date,obj['group_days'])
    credit = dif_day*obj['group__course__price']/12
    student_balance = StudentBalance.objects.filter(Q(title=obj['group__title']) | Q(title='Balans'),student__id=obj['student__id'])
    group_balance = student_balance.exclude(title='Balans').first()
    total_balance = student_balance.get(title='Balans')

    if(credit<=group_balance.balance or total_balance.balance == 0):
                group_balance.balance=group_balance.balance-credit
    elif(credit > group_balance.balance  
    and 
    credit <= group_balance.balance + total_balance.balance ):
        credit=credit-group_balance.balance
        group_balance.balance=0
        total_balance.balance=total_balance.balance-credit
    else:
        credit=credit-total_balance.balance
        total_balance.balance=0
        group_balance.balance=total_balance.balance-credit 
    total_balance.save()    
    group_balance.save()
    monthly_job,_ = Jobs.objects.get_or_create(run_date=end_lesson_date)  
    monthly_job.is_done=True
    monthly_job.save() 

def pay_month(objs):
    today = datetime.now().date()
    first_day = today.replace(day=1)
    last_day = last_day_of_month(first_day)

    for obj in objs:
        if obj['created'].date()>obj['group__start_date']:
            days = cal_days(last_day,first_day,obj['group_days'],bl_check=False) 
            weekday_count=cal_days(obj['created'].date(),first_day,obj['group_days'])
            dif_day = days-weekday_count
            credit = dif_day*obj['group__course__price']/days
            student_balance = StudentBalance.objects.filter(Q(title=obj['group__title']) | Q(title='Balans'),student__id=obj['student__id'])
            group_balance = student_balance.exclude(title='Balans').first()
            total_balance = student_balance.get(title='Balans')

            if(credit<=group_balance.balance or total_balance.balance == 0):
                group_balance.balance=group_balance.balance-credit
            elif(credit > group_balance.balance  
            and 
            credit <= group_balance.balance + total_balance.balance ):
                credit=credit-group_balance.balance
                group_balance.balance=0
                total_balance.balance=total_balance.balance-credit
            else:
                credit=credit-total_balance.balance
                total_balance.balance=0
                group_balance.balance=total_balance.balance-credit 
            total_balance.save()    
            group_balance.save()
            monthly_job,_ = Jobs.objects.get_or_create(run_date=last_day)  
            monthly_job.is_done=True
            monthly_job.save()  

def pay_year(objs):
    pass

def pay_module(objs):
    pass

def pay_take(today):
    global job
    by_lesson = GroupStudents.custom_manager.pay_by_lesson()
    by_month = GroupStudents.custom_manager.pay_by_month()
    by_year = GroupStudents.custom_manager.pay_by_year()
    by_module = GroupStudents.custom_manager.pay_by_module()
    today = today.date()
    first_day = today.replace(day=1)
    last_day = last_day_of_month(first_day)
    
    if by_lesson.exists():
        for obj in by_lesson:
            run_date = str(find_last_lesson(obj['group__start_date'].date(),obj['group_days']))+' 23:50:00'
            scheduler.add_job(pay_month, 'date', run_date=run_date,args=[obj,run_date[:-9]]) 
    if by_month.exists():
        monthly_job,_ = Jobs.objects.get_or_create(run_date=last_day)
        run_date = str(last_day)+' 01:42:15'
        if not monthly_job.is_done:
            job = scheduler.add_job(pay_month, 'date', run_date=run_date,args=[by_month]) 
    if by_year.exists():
        pay_year(by_year)
    if by_module.exists():
        pay_module(by_module)     
                 

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
job = None
step = 0

def start():
    global step
    today = datetime.now()
    b= today + timedelta(0,5)
    b=b.strftime("%Y-%m-%d %H:%M:%S")
    scheduler.add_job(pay_take, 'date', run_date=b,args=[today])
    step+=1
    try:
        scheduler.start()
    except:
        pass