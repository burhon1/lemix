from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse
from datetime import date,datetime
from django.core import serializers
from django.db.models import Q
import json
from admintion.selectors import get_next_n_group_dates
from user.models import CustomUser
from admintion.models import GroupStudents, Room, TaskTypes, Teacher,Course,Group,GroupsDays,Student,Attendace
from admintion.utilts.users import get_days,get_month
from admintion.templatetags.custom_tags import attendance_result
from admintion.services.groups import get_attendace

def groups_view(request):
    context = {}
    if request.method == "POST":
        post = request.POST 
        title = post.get('title',False)
        course = post.get('course',False)
        status = post.get('status',False)
        teacher = post.get('teacher',False)
        room = post.get('room',False)
        trainer = post.get('trainer',False)
        days = post.getlist('days',False)
        pay_type = post.get('pay_type',False)
        start_time = post.get('start_time',False)
        end_time = post.get('end_time',False)
        comments = post.get('comments',False)
        if title and course and status and teacher and room and trainer and days and pay_type and start_time and end_time and comments:
            course = Course.objects.filter(id=course).first()
            teacher = Teacher.objects.filter(id=teacher).first()
            room = Room.objects.filter(id=room).first()
            trainer = Teacher.objects.filter(id=trainer).first()
            days=GroupsDays.objects.filter(id__in=days)
            group = Group(
                title=title,
                comments=comments,
                course=course,
                teacher=teacher,
                trainer=trainer,
                room=room,
                pay_type=pay_type,
                status=status,
                start_time=start_time,
                end_time=end_time
            )
            group.save()
            group.days.add(*days)
            return redirect('admintion:groups')
        else:
            context['error'] = 'Malumotlar to\'liq kiritilmadi'  
            return redirect(reverse('admintion:groups')+f"?error={context['error']}")      
    context['teachers'] = Teacher.objects.filter(teacer_type=True) 
    context['trainers'] = Teacher.objects.filter(teacer_type=False)
    context['rooms'] = Room.objects.all()
    context['courses'] = Course.objects.all()
    context['groups'] = Group.groups.groups()
    return render(request,'admintion/groups.html',context)

def group_detail_view(request,id):
    context = {}
    if request.method == "POST":
        pass
    context['group'] = Group.groups.group(id)
    context = context | get_attendace(id,context['group']['start_date'])
    context['student_list'] = Student.students.studet_list()
    context['task_types'] = TaskTypes.objects.all()
    context['responsibles'] = CustomUser.objects.filter(Q(is_superuser=True)|Q(is_staff=True))
    return  render(request,'admintion/group.html',context)

def get_attendace_view(request):
    context = {}
    data = json.loads(request.body)
    year_month = data['date']
    
    take_date = datetime.strptime(year_month+'-01','%Y-%m-%d') 
    context['group'] = Group.groups.group(data['group_id'])
    context = context | get_attendace(data['id'],context['group']['start_date'],take_date)
    context['students_attendace']=list(context['students_attendace'])
    
    del context['students']
    return JsonResponse({'status':201} | context) 

def change_attendace_view(request):
    data = json.loads(request.body)
    data['status'] = int(data['status'])
    # attendace = Attendace.objects.filter(student__id=data['id'],date=data['date'])
    gr_student, created = GroupStudents.objects.get_or_create(
        student_id=data['id'],group_id=data['group_id'])
    attendace = Attendace.objects.filter(group_student=gr_student,date=data['date'])
    
    if attendace.exists():
        attendace=attendace.first()
        attendace.status=data['status']
        attendace.save()
    else:
        # student=Student.objects.filter(id=data['id']).first()
        # attendace = Attendace(
        #    student=student,
        #    status=data['status'],
        #    date=data['date']
        # )
        attendace = Attendace(
           group_student=gr_student,
           status=data['status'],
           date=data['date'],
           creator=request.user
        )
        attendace.save() 

    return JsonResponse({'status':201,'count':0})

def group_detail_data(request, id: int):
    context = dict()
    context['group'] = Group.groups.group(id)
    context['group']['dates'] = get_next_n_group_dates(10, context['group'])
    print(context['group'])
    return JsonResponse(context)


def add_student_view(request,id):
    context={}
    if request.method == "POST":
        student = request.POST.get('student',False)
        if student:
            print(student)
            return redirect('admintion:group-detail',id=id)
        else:
            context['error'] = 'Malumotlar to\'liq kiritilmadi'  
            return redirect(reverse('admintion:groups')+f"?error={context['error']}")      
    return JsonResponse({'status':201,'count':0}) 
