from admintion.models import Group
from finance.models import StudentBalance,Paid
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

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
    if int(paid_type)>=5:
        student_balance = StudentBalance.objects.filter(title=title,student=student).first()
        if student_balance is None:
            student_balance = StudentBalance.objects.create(title=title,student=student) 
        student_balance.balance=student_balance.balance+int(price)
        student_balance.save()
    return {
        'balance':student_balance.balance,
        'paid_id':paid.pk
    }

def pay_take():
    pass

@sched.scheduled_job('interval', minutes=1)
def start():
	# scheduler = BackgroundScheduler()
	# scheduler.add_job(pay_take, 'interval', min=1)
	# scheduler.start()
    print('Take value')