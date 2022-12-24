from typing import List, Dict
from datetime import time, datetime
from django.forms.models import model_to_dict
from django.db.models import Q
from admintion.models import Student, GroupStudents, Group, Teacher, Room
from education.models import Contents
from admintion.data.chooses import STUDENT_STATUS, GROUPS_DAYS
from finance.models import StudentBalance
def get_student_attendance_percentage(student:Student, gr_student: GroupStudents):
    return round(
        len(gr_student.attendance.filter(status__in=[1, 3])) / (len(gr_student.attendance.all()) or 1),
        ndigits=2
    )*100

def get_percentage(student:Student, gr_student: GroupStudents, attendance_percentage: int=None):
    if attendance_percentage is None:
        attendance_percentage = get_student_attendance_percentage(student, gr_student)
    contents = gr_student.group.contents_set.all()
    return len(contents.filter(students=student))*(len(contents) / 100)+attendance_percentage

def get_student_unseen_lessons(student:Student, group:Group):
    contents = group.contents_set.all()
    lessons = group.lessons_set.exclude(contents__students=student)
    return [lesson.id for lesson in lessons] 


def get_student_payment(student: Student, group:Group):
    payment = StudentBalance.objects.filter(student=student, title=group.title).first()
    return payment.balance if payment else 0

def get_student_report(student: Student=None, id: int=None):
    if student is None and id:
        student = Student.objects.get(id=id)
    data = list()

    for group in student.ggroups.filter(status__in=[1, 2]):
        dct = {
            'group': group.group.title,
            'finished': group.finished,
            'course': group.group.course.title,
            'participating_status': dict(STUDENT_STATUS)[group.status], # Aktiv, Muzlatilgan, Ketgan.
            'homework_balls': '',
            'rate_on_group': '',
            'attendance': get_student_attendance_percentage(student, group),
            'lessons': len(group.group.lessons_set.all()),
            'not_seen_lessons': get_student_unseen_lessons(student, group.group),  # Ishtirok etmagan darslari. 
            
            'payment': get_student_payment(student, group.group)
        }
        dct.update({
            'percentage': get_percentage(student, group, dct['attendance']),
            'lessons_count': dct['lessons']-len(dct['not_seen_lessons']),
        })
        data.append(dct)

    return data

def add_or_change(array, times, group=None):
    try:
        index = array.index({'group':None, 'times':times})
        array[index]['group'] = group
    except ValueError:
        array.append({'group':group, 'times': times})


DAYS = {
    "Dushanba": 1,
    "Seshanba": 2,
    "Chorshanba": 3,
    "Payshanba": 4,
    "Juma": 5,
    "Shanba": 6,
    "Yakshanba": 7,
}


def get_time():
    times = [time(hour=hour, minute=0) for hour in range(7, 20)]
    return [(times[index], times[index+1]) for index in range(len(times)-1)]

def get_group_lessons_by_date(rooms, dates)->List[Dict]:
    times = get_time()
    data, counter = dict(), 1
    for week in dates:
        week1 = []
        for date in week:
            date_data = date
            days = []
            for room in rooms:
                room_data = model_to_dict(room, exclude=('image',))
                room2 = []
                groups = room.group_set.filter(days__days=DAYS[date['day']])
                for tm in times: # time is tuple. start-time and end-time
                    lesson = {'group':None, 'times': time}
                    _not_added = True
                    for group in groups:
                        if group.start_time<= tm[0]< group.end_time:
                            lesson['group'] = group
                        if lesson['group']:
                            _not_added = False
                            add_or_change(room2, tm, group=group)
                            break
                    if _not_added:
                        add_or_change(room2, tm)
                    
                room_data.update({'times': room2})
                days.append(room_data)
            date_data.update({'room':days})
            week1.append(date_data)
        data[f'week-{counter}'] = week1
        counter += 1

    times = [f"{time[0].strftime('%H:%M')}-{time[1].strftime('%H:%M')}" for time in times] 
    return data, times


def get_teacher_lessons_by_date(teachers, dates):
    times = get_time() # list of tuples
    data, counter = dict(), 1
    groups = Group.objects.filter(teacher__in=teachers)

    for week in dates:
        week_data = list()
        for day in week:
            day_data = { 'day': day, 'teachers': []}
            for teacher in teachers:
                teacher_data = {'id': teacher.id, 'full_name': teacher.user.full_name(), 'times':[]}
                for tm in times:
                    lesson = {'group':None, 'times': time}
                    _not_added = True
                    for group in teacher.group_teacher.filter(days__days=DAYS[day['day']]):
                        if group.start_time<= tm[0]< group.end_time:
                            lesson['group'] = group
                        if lesson['group']:
                            _not_added = False
                            add_or_change(teacher_data['times'], tm, group=group)
                            break
                    if _not_added:
                        add_or_change(teacher_data['times'], tm)
                day_data['teachers'].append(teacher_data)
            week_data.append(day_data)
        data[counter] = week_data
        counter+=1 
    return data


def get_teacher_schedule_by_date(teacher:Teacher, dates)->List[Dict]:
    times = get_time()
    full_data, data, counter =dict(), dict(), 1
    groups = Group.objects.prefetch_related('days').filter(Q(teacher=teacher)|Q(trainer=teacher), status__lt=5)
    rooms = Room.objects.filter(educenter=teacher.user.educenter)
    for week in dates: # for rooms
        week1 = []
        for date in week:
            date_data = date
            
            days = []
            for room in rooms:
                room_data = model_to_dict(room, fields=('id','title'))
                room2 = []
                room_groups = groups.filter(room=room, days__days=DAYS[date['day']])
                for tm in times: # time is tuple. start-time and end-time
                    lesson = {'group':None, 'times': time}
                    _not_added = True
                    for group in room_groups:
                        if group.start_time<= tm[0]< group.end_time:
                            lesson['group'] = group
                        if lesson['group']:
                            _not_added = False
                            add_or_change(room2, tm, group=group)
                            continue
                    if _not_added:
                        add_or_change(room2, tm)
                    
                room_data.update({'times': room2})
                days.append(room_data)
            
            
            
            
            date_data.update({'room':days})
            week1.append(date_data)
        data[f'week-{counter}'] = week1
        counter += 1

     
    
    
    full_data['rooms'] = data
    data2 = {}
    counter = 1
    for week in dates:  # for groups
        week1 = []
        for date in week:
            date_data = date
            days = []
            
            # room_groups = groups.filter(days__days=DAYS[date['day']])
            for group in groups:
                room_data = model_to_dict(group, fields=('title', 'course__title', ))
                room2, _on_other_day = [], False
                
                if DAYS[date['day']] not in [day.days for day in group.days.all()]:
                    _on_other_day = False
                for tm in times: # time is tuple. start-time and end-time
                    lesson = {'group':None, 'times': time}
                    _not_added = True
                    if group.start_time<= tm[0]< group.end_time and not _on_other_day:
                        lesson['group'] = group
                    if lesson['group']:
                        _not_added = False
                        add_or_change(room2, tm, group=group)
                        continue
                    if _not_added:
                        add_or_change(room2, tm)
                    print(lesson, "\n")
                    
                room_data.update({'times': room2})
                days.append(room_data)
            
            
            
            
            date_data.update({'groups':days})
            week1.append(date_data)
        data2[f'week-{counter}'] = week1
        counter += 1
    times = [f"{time[0].strftime('%H:%M')}-{time[1].strftime('%H:%M')}" for time in times]
    full_data['times'] = times
    full_data['groups'] = data2

    return full_data