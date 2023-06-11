from django.shortcuts import get_object_or_404

from finance.models import StudentBalance
from admintion.models import Group, Parents, Student, GroupStudents, Sources


def set_student_group(student: Student, group: Group,attend_date):
    # message: str = "Muvaffaqiyatli yaratildi"
    try:
        GroupStudents.objects.create(student=student, group=group,attend_date=attend_date)
        StudentBalance.objects.create(student=student, title=group.title)
    except:
        pass# message = "talaba guruhga avvaldan biriktirilgan"
    return


def set_student_group_status(student_id, id, status: int):
    from django.db.models import Sum
    student_balances = StudentBalance.objects.filter(student__id=student_id)
    group_balances_sum=0
    current_balance = student_balances.filter(title='Balans').first().balance
    if type(id) == str and id == "umumiy":
        objs =  GroupStudents.objects.filter(student_id=student_id).exclude(status=status)
        objs.update(status=status)
        
        group_balances = student_balances.exclude(title='Balans')
        group_balances_sum=group_balances.aggregate(Sum('balance'))
        group_balances.delete()
    else:
        student_group = get_object_or_404(GroupStudents, id=id, student_id=student_id)
        if 1 <= status <=3:
            student_group.status = status
            student_group.save()
            group_balances_sum=student_balances.filter(title=student_group.group.title).aggregate(Sum('balance'))
    student_balances.filter(title='Balans').update(balance=current_balance+group_balances_sum['balance__sum'])

def update_student(student_id, data):
    student = get_object_or_404(Student, pk=student_id)
    source = get_object_or_404(Sources, pk=int(data.get('source')))
    student.source = source or student.source
    student.comment = data.get('comment', student.comment)
    
    user = student.user
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.middle_name = data.get('middle_name', user.middle_name)
    user.phone = str(data.get('phone', user.phone)).replace('+998', '')
    user.location = data.get('location', user.location)
    user.email = data.get('email', user.email)

    student.save()
    user.save()

def update_parent(parent_id, data):
    parent = get_object_or_404(Parents, pk=parent_id)
    parent.phone = data.get('passport', parent.passport)
    parent.telegram = data.get('telegram', parent.telegram)
    
    user = parent.user
    user.first_name = data.get('full_name'[1], user.first_name)
    user.last_name = data.get('full_name'[0], user.last_name)
    user.phone = str(data.get('phone', user.phone)).replace('+998', '')

    parent.save()
    user.save()