from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q,F
from django.urls import reverse
from django.http import JsonResponse
from admintion.utils import get_list_of_dict,get_list_of_filter
from finance.models import StudentBalance,Paid
from user.services.users import user_add, CustomUser
from django.contrib.auth.models import Group
from django.utils import timezone
import json
from admintion.models import EduCenters,UserTaskStatus,Course,Student,Teacher, Group as GroupModel,GroupStudents, Parents, TaskTypes, Sources, Tasks
from admintion.selectors import get_student_courses, get_student_groups, get_student_attendaces, get_student_unwritten_groups,get_student_report
from admintion.services.student import set_student_group, set_student_group_status, update_student
from admintion.templatetags.custom_tags import readable_days
from admintion.data.chooses import STUDENT_STATUS

def students_view(request):
    context = {}
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter = EduCenters.objects.filter(qury)
    if request.method == "POST":
        if educenter.count() == 1:
            post = request.POST
            groups = Group.objects.filter(name="Student")
            status,obj = user_add(groups,request).values()
            source=post.get('source',False)
            comment=post.get('comment',False)
            if status==200 and source:
                student = Student(
                    source=get_object_or_404(Sources, pk=int(source)),
                    user=obj,
                    educenter=educenter.first()
                )
                if comment:
                    student.comment=comment
                student.save()
                StudentBalance.objects.create(student=student, title="Balans")
                parent = post.get('parent_name',False)
                pphone = post.get('parent_phone',False)
                telegram = post.get('telegram_telegram',None)
                passport = post.get('passport_passport', None)
                group = post.get('group',False)
                attend_date = post.get('attend',False) 
                task_date = post.get('task_date', None)
                task_comment = post.get('task_comment', None)
                task_who = post.get('task_who', None)
                task_type = post.get('task_type', None)
                if parent and pphone:
                    parent_user,created = CustomUser.objects.get_or_create(phone=pphone.replace("+998",""))
                    parent_user.first_name = parent
                    if parent_user.password == '':
                        parent_user.set_password(pphone)
                    parent_user.save()
                    parent, created = Parents.objects.get_or_create(user=parent_user)
                    parent.telegram = telegram or parent.telegram
                    parent.passport = passport or parent.passport
                    parent.educenter=educenter.first()
                    parent.students.add(student)
                    parent.save()
                if group:
                    grop = GroupModel.objects.get(id=group)
                    set_student_group(student, grop,attend_date)
                if task_date and task_who and task_type:
                    whom=CustomUser.objects.get(pk=task_who)
                    task_type=TaskTypes.objects.get(id=task_type)
                    user_task = UserTaskStatus.objects.filter(whom="Student").first()
                    task = Tasks(
                        comment=task_comment,
                        deadline=task_date,
                        author=request.user,
                        task_type=task_type,
                        educenter=educenter.first(),
                        user_status=user_task
                    )
                        
                    task.save()    
                return redirect('admintion:students')
            else:
                context['error'] = 'Malumotlar to\'liq kiritilmadi'  
                return redirect(reverse('admintion:students')+f"?error={context['error']}")
        return redirect(reverse('admintion:teachers')+f"?error=Filyalni tanlang") 
    educenter_ids=educenter.values_list('id',flat=True)
    context['students'] = Student.students.students(educenter_ids)
    # context['groups_list'] = GroupModel.groups.groups(educenter_ids,short_info=True)
    context['sources'] = Sources.objects.all()
    context['students_count'] = context['students'].count()
    context=context|context['students'].students_by_status()
    context['datas_of_teacher'] = list(Teacher.teachers.teacher_list(educenter_ids))
    context['datas_of_group'] = list(GroupModel.groups.group_list(educenter_ids))
    context['datas_of_course'] = list(Course.courses.courses(educenter_ids,True))
    context['datas_of_status'] = get_list_of_dict(('id','title'),STUDENT_STATUS)
    context['keys'] = ['check','title','course','teacher','days','times','total_student','course__price','action']
    context['task_types'] = list(TaskTypes.objects.annotate(title=F('task_type')).values('id', 'title'))
    context['task_responsibles'] = list(CustomUser.users.get_user_list({'groups__name__in':['Admintion','Director','Manager','Teacher']},educenter_ids))
    return render(request,'admintion/students.html',context) 

def students_archive_view(request):
    context = {}
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter = EduCenters.objects.filter(qury)
    educenter_ids=educenter.values_list('id',flat=True)
    context['students'] = Student.students.students_archive(educenter_ids)
    # context['groups_list'] = GroupModel.groups.groups(educenter_ids,short_info=True)
    context['sources'] = Sources.objects.all()
    context['students_count'] = context['students'].count()
    context=context|context['students'].students_by_status()
    context['datas_of_teacher'] = list(Teacher.teachers.teacher_list(educenter_ids))
    context['datas_of_group'] = list(GroupModel.groups.group_list(educenter_ids))
    context['datas_of_course'] = list(Course.courses.courses(educenter_ids,True))
    context['datas_of_status'] = get_list_of_dict(('id','title'),STUDENT_STATUS)
    context['keys'] = ['check','title','course','teacher','days','times','total_student','course__price','action']
    context['task_responsibles'] = list(CustomUser.users.get_user_list({'groups__name__in':['Admintion','Director','Manager','Teacher']},educenter_ids))
    return render(request,'admintion/students.html',context) 

def student_by_filter_view(request):
    context={}
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter_ids = EduCenters.objects.filter(qury).values_list('id',flat=True)   

    status = request.GET
    filter_keys=get_list_of_filter(status)
    student = list(Student.students.student_filter(filter_keys,educenter_ids).values())
    return JsonResponse({'data':student,'status':200})

def student_detail_view(request,id):
    context = {}
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter = EduCenters.objects.filter(qury)
    if request.method == "POST":
        post = request.POST.get('student')
        update_student(id, json.loads(post))
    educenter_ids=educenter.values_list('id',flat=True)
    context['student'] = Student.students.student_detail(id,educenter_ids)
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
    #return JsonResponse({'status': status})
    return redirect('admintion:students')

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


def student_change_status(request,id):
    student = get_object_or_404(Student, pk=id)
    student.status=3
    student.save()
    return JsonResponse({"status":203})