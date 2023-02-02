from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse
from admintion.utils import get_list_of_dict,get_list_of_filter
from finance.models import StudentBalance,Paid
from user.services.users import user_add, CustomUser
from django.contrib.auth.models import Group
from django.utils import timezone
import json
from admintion.models import EduCenters,Course,Student,Teacher, Group as GroupModel,GroupStudents, Parents, TaskTypes, Sources, Tasks
from admintion.selectors import get_student_courses, get_student_groups, get_student_attendaces, get_student_unwritten_groups,get_student_report
from admintion.services.student import set_student_group, set_student_group_status, update_student
from admintion.templatetags.custom_tags import readable_days
from admintion.data.chooses import STUDENT_STATUS

def students_view(request):
    context = {}
    if request.method == "POST":
        post = request.POST
        groups = Group.objects.filter(name="Student")
        status,obj = user_add(groups,request).values()
        source=post.get('source',False)
        comment=post.get('comment',False)
        if status==200 and source:
            student = Student(
                source=get_object_or_404(Sources, pk=int(source)),
                comment=comment,
                user=obj
            )
            student.save()
            StudentBalance.objects.create(student=student, title="Balans")
            parent = post.get('parent_name',False)
            pphone = post.get('parent_phone',False)
            telegram = post.get('telegram_telegram',None)
            passport = post.get('passport_passport', None)
            group = post.get('group',False)
            if parent and pphone:
                try:
                    fname, lname = parent.split(" ")
                except ValueError:
                    fname,lname = parent,''
                data = {'first_name':fname, 'last_name':lname, 'phone':pphone}
                parent_user,created = CustomUser.objects.get_or_create(phone=pphone)
                parent_user.first_name = fname or parent_user.first_name
                parent_user.last_name = lname or parent_user.last_name
                if parent_user.password == '':
                    parent_user.set_password(pphone)
                parent_user.save()
                parent, created = Parents.objects.get_or_create(user=parent_user)
                parent.telegram = telegram or parent.telegram
                parent.passport = passport or parent.passport
                parent.students.add(student)
                parent.save()
            if group:
                grop = GroupModel.objects.get(id=group)
                set_student_group(student, grop)
            return redirect('admintion:students')
        else:
            context['error'] = 'Malumotlar to\'liq kiritilmadi'  
            return redirect(reverse('admintion:students')+f"?error={context['error']}")
    ed_id=request.user.educenter
    branch_id = int(request.session.get('branch_id',False))
    if branch_id == 0:
        educenter_ids = EduCenters.objects.filter(id=ed_id).values_list('id',flat=True)|EduCenters.objects.filter(parent__id=ed_id).values_list('id',flat=True)              
    else:
        educenter_ids = [branch_id]
    
    context['students'] = Student.students.students(educenter_ids)
    context['sources'] = Sources.objects.all()
    context['students_count'] = context['students'].count()
    context=context|context['students'].students_by_status()
    context['datas_of_teacher'] = list(Teacher.teachers.teacher_list(educenter_ids))
    context['datas_of_group'] = list(GroupModel.groups.group_list(educenter_ids))
    context['datas_of_course'] = list(Course.courses.courses(educenter_ids,True))
    context['datas_of_status'] = get_list_of_dict(('id','title'),STUDENT_STATUS)
    return render(request,'admintion/students.html',context) 

def student_by_filter_view(request):
    context={}
    ed_id=request.user.educenter
    branch_id = int(request.session.get('branch_id',False))
    if branch_id == 0:
        educenter_ids = EduCenters.objects.filter(id=ed_id).values_list('id',flat=True)|EduCenters.objects.filter(parent__id=ed_id).values_list('id',flat=True)              
    else:
        educenter_ids = [branch_id]

    status = request.GET
    filter_keys=get_list_of_filter(status)

    student = list(GroupStudents.custom_manager.student_filter(filter_keys,educenter_ids))
    return JsonResponse({'data':student,'status':200})

def student_detail_view(request,id):
    context = {}
    if request.method == "POST":
        post = request.POST.get('student')
        update_student(id, json.loads(post))
    context['student'] = Student.students.student_detail(id)
    context['parent'] = Parents.parents.parent(id)
    context['courses'] = get_student_courses(id)
    context['groups'] = get_student_groups(id)
    context['attendaces'], context['attendace_results'] = get_student_attendaces(id)

    context['responsibles'] = CustomUser.objects.filter(Q(is_superuser=True)|Q(is_staff=True))
    context['task_types'] = TaskTypes.objects.all()
    context['balances'] = StudentBalance.objects.filter(student=context['student']['id'])
    context['paids'] = Paid.objects.filter(student__id=context['student']['id'])
    context['tasks'] = Tasks.tasks.student_tasks(id)
    context['today_tasks'] = len([task for task in context['tasks'] if task['deadline'].date() == timezone.now().date()])
    context['reports'] = get_student_report(id=id)
    return render(request,'admintion/student_detail.html',context)

def student_view(request,id):
    context = {}
    return render(request,'admintion/student.html',context)

def student_add_group_view(request, id):
    student = get_object_or_404(Student, pk=id)
    data = dict()
    if request.method == "POST":
        post = request.POST
        group = get_object_or_404(GroupModel, pk=post['group'])
        set_student_group(student, group)
    data['groups'] = list(get_student_unwritten_groups(id))
    return JsonResponse(data)

def student_deactivate_view(request, id):
    data = dict()
    if request.method == 'POST':
        post = request.POST
        set_student_group_status(id, post['group_student'], status=2)
    data['groups'] = list(get_student_groups(id).filter(status=1).values('id', 'group__title'))
    return JsonResponse(data)

def student_remove_view(request, id):
    data = dict()
    if request.method == 'POST':
        post = request.POST
        set_student_group_status(id, post['group_student'], status=3)
    data['groups'] = list(get_student_groups(id).filter(status__lt=3).values('id', 'group__title'))
    return JsonResponse(data)

def student_activate_view(request, id):
    if request.method == 'POST':    
        set_student_group_status(id, "umumiy", status=1)
    return JsonResponse({"status": 200})


def student_delete_view(request, id):
    student = get_object_or_404(Student, pk=id)
    status = 400
    if request.method == 'POST':
        student.delete()
        # print(student._meta.related_objects)
        status = 302
        # for related_object in student._meta.related_objects:
        #     print(related_object.first())
    return JsonResponse({'status': status})

def student_add_task_view(request, id):
    return JsonResponse({"detail":'success', 'status':201})

def student_detail_data(request, id: int):
    student = get_object_or_404(Student, pk=id)
    groups = list()
    for group in student.ggroups.all():
        groups.append(f"{group.group.title} | {readable_days(group.group)} | {group.group.start_time.strftime('%H:%M')}-{group.group.end_time.strftime('%H:%M')}")

    context = {
        'full_name': student.user.full_name(),
        'phone_number': f"+998 {student.user.phone[:2]} {student.user.phone[2:]}",
        'groups': groups
    }
    return JsonResponse(context, safe=False)