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
            goal_type=goal_type,
            description=description,
            user=user
        )
    title=None
    if goal_type!="0":
        group = Group.objects.filter(id=goal_type).first()
        paid.group=group
        title=group.title
    else:
        title="Balans"
    student_balance = StudentBalance.objects.filter(title=title,student=student).first()
    student_balance.balance=student_balance.balance+int(price)
    paid.save()
    student_balance.save()
    return student_balance.balance

def pay_take():
    pass

@sched.scheduled_job('interval', minutes=1)
def start():
	# scheduler = BackgroundScheduler()
	# scheduler.add_job(pay_take, 'interval', min=1)
	# scheduler.start()
    print('Take value')