from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Attendace, Student, Course, Group, GroupStudents
from .templatetags.custom_tags import attendance_result
def convert_str(_iterable, counter=0):
    try:
        if counter > 0:
            return f", {_iterable[counter]}{convert_str(_iterable, counter=counter+1)}"
        return f"{_iterable[counter]}{convert_str(_iterable, counter=counter+1)}"
    except:
        return ""

def get_student_courses(student_id: int, type="iterable"):
    student = get_object_or_404(Student, pk=student_id)
    if student.groups:
        courses = set()
        for group in student.groups.all():
            try:
                courses.add(group.course.title)
            except:
                pass
        return convert_str(list(courses))
        # return courses
    return ""


def get_student_groups(student_id: int):
    student_groups = GroupStudents.objects.filter(student_id=student_id)
    return student_groups


def get_student_attendaces(student_id: int):
    group_students = GroupStudents.objects.filter(student_id=student_id)
    
    ids = [ _.id for _ in group_students]

    attendaces = Attendace.objects.filter(group_student_id__in=ids).only(
        'id', 'group_student', 'status', 'date', 'creator', 'created').order_by('-date')
    
    # get percentage
    results = list()
    for _ in group_students:
        objs = attendaces.filter(group_student=_)
        count=0
        if objs.exists():
            goal = objs.filter(status=1)
            count = goal.count()/objs.count()
        results.append(
            {'group': _.group.title, 'percentage': int(count*100)}
        )

    return attendaces, results

def get_student_unwritten_groups(student_id: int):
    groups = get_student_groups(student_id)
    return Group.objects.exclude(
                Q(id__in=[group.group.id for group in groups])|
                Q(status__gt=4)).values('id', 'title')