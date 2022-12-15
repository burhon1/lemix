from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from admintion.utilts.calendar_weeks import week_dates
from admintion.selectors.hisobot import get_group_lessons_by_date, get_teacher_lessons_by_date
from admintion.models import Room, Group, Teacher

@login_required
def reports_view(request):
    now = timezone.now()
    dates = week_dates(now.year, now.month)
    rooms = Room.objects.all()
    group_lessons, times = get_group_lessons_by_date(rooms, dates)
    teachers = Teacher.objects.filter(teacer_type=True)
    teacher_lessons = get_teacher_lessons_by_date(teachers, dates)
    rooms = {
        'dates': dates,
        'schedule': group_lessons,
        'times': times
    }
    teachers = {
        'schedule': teacher_lessons
    }
    context = {
        'rooms':rooms,
        'teachers': teachers,
        
    }
    return render(request, 'admintion/dars_jadvali.html', context)