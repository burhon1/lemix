from admintion.models import GroupStudents,Group
from finance.models import StudentBalance,Paid
from datetime import datetime
from django.db.models import Q
import calendar
from datetime import datetime,timedelta

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

def last_day_of_month(any_day):
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = any_day.replace(day=28) + timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return next_month - timedelta(days=next_month.day)

def cal_days(day1,day2,group_days,bl_check=True):
    weekday_count = 0
    cal = calendar.Calendar()

    for week in cal.monthdayscalendar(day1.year, day1.month):
        for i, day in enumerate(week):
            # not this month's day or a weekend
            # print(day1.day,day)
            if day == 0 or (i+1 not in group_days):
                continue
            # or some other control if desired...
            if int(day1.day)<=day and bl_check:
                return weekday_count
            weekday_count += 1
    return weekday_count        

def pay_lesson(objs):
    pass

def pay_month(objs):
    # print(objs)
    today = datetime.now().date()
    first_day = today.replace(day=1)
    last_day = last_day_of_month(first_day)
       
    for obj in objs:
        # print(obj)
        if obj['created'].date()>obj['group__start_date']:
            days = cal_days(last_day,first_day,obj['group_days'],bl_check=False) 
            weekday_count=cal_days(obj['created'].date(),first_day,obj['group_days'])
            dif_day = days-weekday_count
            # print(days,weekday_count)
            print(dif_day*obj['group__course__price']/days)
            # print(obj['created'].date())

def pay_year(objs):
    pass

def pay_module(objs):
    pass

def pay_take():
    by_lesson = GroupStudents.custom_manager.pay_by_lesson()
    by_month = GroupStudents.custom_manager.pay_by_month()
    by_year = GroupStudents.custom_manager.pay_by_year()
    by_module = GroupStudents.custom_manager.pay_by_module()
    
    if by_lesson.exists():
        pay_lesson(by_lesson)
    if by_month.exists():
        pay_month(by_month)
    if by_year.exists():
        pay_year(by_year)
    if by_module.exists():
        pay_module(by_module)            

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
job = None


def start():
    global job
    job = scheduler.add_job(pay_take, 'interval', seconds=5)
    try:
        scheduler.start()
    except:
        pass