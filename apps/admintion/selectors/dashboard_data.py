from django.db.models import Q
import calendar
from user.models import CustomUser
from admintion.models import EduCenters, FormLead, LeadDemo, Group, Student, GroupStudents, Tasks, Course
from admintion.utilts.calendar_weeks import week_dates
from admintion.selectors.hisobot import get_time, get_teacher_schedule_by_date
from django.utils import timezone

def get_data_to_director(user:CustomUser):
    educenter = EduCenters.objects.filter(director=user).first()
    if educenter is None:
        return dict()
    educenter = educenter.id
    students = Student.objects.filter(user__educenter=educenter)
    fin_students_per = len(GroupStudents.objects.filter(group__status=5, student__user__educenter=educenter))//(len(students) or 1)*100
    rem_students_per = len(GroupStudents.objects.filter(status=3, student__user__educenter=educenter))//(len(students) or 1)*100

    data = {
        'educenter': educenter,
        'active_leads': FormLead.objects.filter(user__educenter=educenter, activity=1),
        'active_demos': LeadDemo.objects.filter(lead__user__educenter=educenter, lead__activity=1).distinct(),
        'groups': Group.objects.filter(educenter=educenter),
        'active_students': students.filter(status=1),
        'active_students_perc': len(students.filter(status=1))//(len(students) or 1)*100,
        'finished_students_perc': fin_students_per,
        'removed_students_perc': rem_students_per,
        'waiting_students': len(GroupStudents.objects.filter(student__user__educenter=educenter, group__status=1))//(len(students) or 1)*100, 
        'current_paid': 0,
        'on_debt': 0,
        'stopped_demo': 0,
        'freezed_students': students.filter(status=2),
        'removed_students': students.filter(status=3),
        'students': len(students),
        'income': 0,
        'debt': 0, 
    }

    courses_data = list()
    courses = Course.objects.filter(educenter=educenter)
    for course in courses:
        group_students = GroupStudents.objects.filter(group__course=course, status=1)
        courses_data.append({
            'id': course.id, 'title':course.title, 'students': len(group_students)
        })
    data.update({
        'courses': courses_data
    })

    return data


def get_data_to_teacher(user:CustomUser):
    educenter = user.educenter
    if educenter is None:
        return dict()

    teacher = user.teacher_set.last()
    if teacher is None:
        return dict()

    groups = Group.objects.filter(Q(teacher=teacher)|Q(trainer=teacher))
    students = GroupStudents.objects.filter(group__in=groups)

    data = {
        'educenter': educenter,
        'active_demos': LeadDemo.objects.filter(lead__user__educenter=educenter, lead__activity=1).distinct(),
        'groups': groups,
        'active_students': students.filter(student__status=1),
        'removed_students': students.filter(status=3),
        'tasks': user.my_tasks.all(),
        'stopped_demo': 0,
        'freezed_students': students.filter(student__status=2),
        'students': len(students),
    }

    tasks = Tasks.tasks.teacher_user_tasks(user.id)
    data.update({'tasks': tasks})

    now = timezone.now()
    weeks = week_dates(now.year, now.month)
    data.update({
        'weeks': weeks,
        'schedule': get_teacher_schedule_by_date(teacher, weeks)
    })

    return data


def get_data_to_admin(user:CustomUser):
    data = {

    }

    return data


def get_data_to_manager(user:CustomUser):
    data = {

    }

    return data



def get_dates():
    data = {
        'curr_week': '',
        'last_week': '',
        'curr_month': '',
        'last_quarter': '',
        'half_a_year': ''    
    }

    return data