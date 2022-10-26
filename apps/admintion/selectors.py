from django.db.models import Q
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime
from .models import Attendace, Student, Course, Group, GroupStudents, FormLead, LeadDemo, Tasks
from .templatetags.custom_tags import attendance_result
from admintion.data.chooses import TASK_STATUS, GET_GROUPS_DAYS

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


def get_form_leads(filters=None, fields=None):
    if filters:
        leads = FormLead.objects.filter(**filters)
    else:
        leads = FormLead.objects.all()
    if fields:
        return leads.values(*fields)
    return leads.values()

def get_demos(lead: FormLead):
    demos = LeadDemo.objects.filter(lead=lead) #.values('id', 'group_id', 'group__title', 'date')
    groups = set([demo.group for demo in demos])

    result = []
    for group in groups:
        demo_objs = demos.filter(group=group).values('date')
        result.append({'group': group.title, 'group_id':group.id, 'dates':demo_objs})
    return result


def set_tasks_status(tasks):
    for task in tasks:
        if task.status == 1 and task.deadline < timezone.now():
            task.status = 3
    
    tasks.filter(status=1, deadline__lte=timezone.now()).update(status=3)
    return tasks


def get_lead_tasks(lead:FormLead=None, tasks:Tasks=None):
    tasks = Tasks.objects.filter(Q(whom__in=[lead.user])|Q(leads__in=[lead])).order_by('-deadline')
    tasks = set_tasks_status(tasks)
    data = list()
    for task in tasks:
        dct = model_to_dict(task, fields=('id','task_type', 'task_type__task_type', 'deadline', 'comment','user_status', 'status', 'created_at'))
        dct['responsibles'] = task.responsibles.all().values('id', 'first_name', 'last_name')
        dct['task_type__task_type'] = task.task_type.task_type
        dct['created_at'] = task.created_at
        dct['status'] = dict(TASK_STATUS)[task.status]
        data.append(dct)
    print(data)
    return data


def get_next_lesson_date(demo:LeadDemo):
    group = demo.group
    group_days = [day.days for day in group.days.all()]
    group_times = [group.start_time, group.end_time]
    now = datetime.datetime.now()

    while True:
        if now.weekday() in group_days and LeadDemo.objects.filter(lead=demo.lead, group=demo.group, date=now.date()).exists() is False:
            return now
        else:
            now+=datetime.timedelta(days=1)


def check_group_limit(group):
    if type(group) == dict:
        group = Group.objects.filter(pk=group['id'] or group['pk']).first()
    if group is None or type(group) != Group:
        return False

    students = len(GroupStudents.objects.filter(group=group))
    demos = LeadDemo.objects.filter(group=group)
    leads = len(set([demo.lead for demo in demos if demo.lead.activity==1])) #  bu guruhga qo'shilgan lidlar soni
    print(students, leads, group.limit)
    return group.limit > students+leads

def select_groups_by_limit(groups):
    selected = [group for group in groups if check_group_limit(group)]
    return selected

def get_next_n_group_dates(n:int, group):
    if type(group) == dict:
        group = Group.objects.filter(id=group['id'] or group['pk']).first()
    group_days = [day.days for day in group.days.all().order_by('days')]
    now = datetime.datetime.now()
    dates, index, step = [], 0, 0
    while len(dates)< n:
        curr_day = now.weekday() + 1
        if curr_day in group_days:
            dates.append({'date':now.date(), 'day':dict(GET_GROUPS_DAYS)[curr_day]})
            index = group_days.index(curr_day)
            step = group_days[index+1] - curr_day if len(group_days) > index+1 else group_days[0]
            now += datetime.timedelta(days=step or 1)
        else:
            now+=datetime.timedelta(days=step or 1)

    return dates