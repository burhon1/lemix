from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, Http404
from datetime import date,datetime
from django.utils import timezone
from django.db.models import Q
import json
from admintion.selectors import get_next_n_group_dates
from user.models import CustomUser
from admintion.models import GroupStudents, LeadDemo,EduCenters, Room, TaskTypes, Teacher,Course,Group,GroupsDays,Student,Attendace,Tasks
from admintion.utilts.users import get_days,get_month
from admintion.templatetags.custom_tags import attendance_result
from admintion.services.groups import get_attendace
from admintion.forms.groups import GroupForm
from finance.models import StudentBalance

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
        start_date = post.get('start_date',False)
        start_time = post.get('start_time',False)
        end_time = post.get('end_time',False)
        comments = post.get('comments',False)
        limit = post.get('limit', False)
        print(days)
        if title and course and status and teacher and room and days and pay_type and start_time and start_date and end_time and comments:
            course = Course.objects.filter(id=course).first()
            teacher = Teacher.objects.filter(id=teacher).first()
            room = Room.objects.filter(id=room).first()
            days=GroupsDays.objects.filter(id__in=days)
            group = Group(
                title=title,
                comments=comments,
                course=course,
                teacher=teacher,
                room=room,
                pay_type=pay_type,
                status=status,
                start_time=start_time,
                end_time=end_time,
                limit=limit,
                start_date=start_date
            )
            if trainer:
                trainer = Teacher.objects.filter(id=trainer).first()
                group.trainer=trainer
            group.save()
            group.days.add(*days)
            return redirect('admintion:groups')
        else: 
            context['error'] = 'Malumotlar to\'liq kiritilmadi'  
            return redirect(reverse('admintion:groups')+f"?error={context['error']}")      
    context['teachers'] = Teacher.objects.filter(teacer_type=True) 
    context['trainers'] = Teacher.objects.filter(teacer_type=False)
    ed_id=request.user.educenter
    educenter_ids = EduCenters.objects.filter(id=ed_id).values_list('id',flat=True)|EduCenters.objects.filter(parent__id=ed_id).values_list('id',flat=True)              
    context['rooms'] = Room.rooms.rooms(educenter_ids)
    context['courses'] = Course.objects.all()
    context['groups'] = Group.groups.groups()
    return render(request,'admintion/groups.html',context)

def group_list_view(request):
    # added_group = GroupStudents.custom_manager.student_add_group(request.user)
    groups = Group.groups.groups(True)
    return JsonResponse({'data':list(groups)})

def group_detail_view(request,id):
    group1 = get_object_or_404(Group, pk=id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group1)
        if form.is_valid():
            form.save()
            return redirect(reverse('admintion:group-detail', args=[id])+"?success=Muvaffaqiyatli yangilandi.")
        else:
            return redirect(reverse('admintion:group-detail', args=[id])+"?error=Ma'lumotlar to'liq emas.")
    group = Group.groups.group(id)
    if group is None:
        raise Http404("Bunday guruh mavjud emas.")
    context = {'date': timezone.now().date(), 'form': GroupForm(), 'group':group, 'group_obj':group1}
    context = context | get_attendace(id,context['group']['start_date'])
    context['student_list'] = Student.students.studet_list()
    context['tasks'] = Tasks.tasks.group_tasks(id=id)
    context['today_tasks'] = len([task for task in context['tasks'] if task['deadline'].date() == timezone.now().date()])
    context['task_types'] = TaskTypes.objects.all()
    context['responsibles'] = CustomUser.objects.filter(Q(is_superuser=True)|Q(is_staff=True))
    context['balances'] = StudentBalance.objects.filter(title=context['group']['title'])
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
        attendace = Attendace(
           group_student=gr_student,
           status=data['status'],
           date=data['date'],
           creator=request.user
        )
        attendace.save() 

    return JsonResponse({'status':201,'count':0})

def change_lead_attendace_view(request):
    data = json.loads(request.body)
    data['status'] = int(data['status'])
    lead_demo, created = LeadDemo.objects.get_or_create(
        lead_id=data['id'],group_id=data['group_id'], date=data['date'])
    attendace = Attendace.objects.filter(lead_demo=lead_demo,date=data['date'])
    
    if attendace.exists():
        attendace=attendace.first()
        attendace.status=data['status']
        attendace.save()
    else:
        attendace = Attendace(
           lead_demo=lead_demo,
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
    return JsonResponse(context)


def add_student_view(request,id):
    context={}
    if request.method == "POST":
        student = request.POST.get('student',False)
        if student:
            return redirect('admintion:group-detail',id=id)
        else:
            context['error'] = 'Malumotlar to\'liq kiritilmadi'  
            return redirect(reverse('admintion:groups')+f"?error={context['error']}")      
    return JsonResponse({'status':201,'count':0}) 
