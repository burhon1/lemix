from django.shortcuts import get_object_or_404
from ..models import Group, Student, GroupStudents


def set_student_group(student: Student, group: Group):
    # message: str = "Muvaffaqiyatli yaratildi"
    try:
        GroupStudents.objects.create(student=student, group=group)
    except:
        pass# message = "talaba guruhga avvaldan biriktirilgan"
    return


def set_student_group_status(student_id, id, status: int):
    if type(id) == str and id == "umumiy":
        GroupStudents.objects.filter(student_id=student_id).exclude(status=status).update(status=status)
    
    else:
        student_group = get_object_or_404(GroupStudents, id=id, student_id=student_id)
        if 1 <= status <=3:
            student_group.status = status
            student_group.save()


def update_student(student_id, data):
    student = get_object_or_404(Student, pk=student_id)
    student.source = int(data.get('source')) or student.source
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