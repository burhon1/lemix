from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse
from user.services.users import user_add, CustomUser
from django.contrib.auth.models import Group
import json
from admintion.models import Student, Group as GroupModel, Parents, TaskTypes
from ..selectors import get_student_courses, get_student_groups, get_student_attendaces, get_student_unwritten_groups
from ..services.student import set_student_group, set_student_group_status, update_student
def students_view(request):
    context = {}
    if request.method == "POST":
        post = request.POST
        groups = Group.objects.filter(name="Student")
        status,obj = user_add(groups,post).values()
        source=post.get('source',False)
        comment=post.get('comment',False)
        if status==200 and source and comment:
            student = Student(
                source=source,
                comment=comment,
                user=obj
            )
            student.save()
            return redirect('admintion:students')
        else:
            context['error'] = 'Malumotlar to\'liq kiritilmadi'  
            return redirect(reverse('admintion:students')+f"?error={context['error']}")
    context['students'] = Student.students.students()
    context['students_count'] = context['students'].count()
    context['active_students'] = context['students'].students_by_status(status=1).count()
    context['nonactive_students'] = context['students'].students_by_status(status=2).count()
    context['removed_students'] = context['students'].students_by_status(status=3).count()
    return render(request,'admintion/students.html',context) 


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
    return render(request,'admintion/student_detail.html',context)


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
        status = 302
    return JsonResponse({'status': status})

def student_add_task_view(request, id):
    return JsonResponse({"detail":'success', 'status':201})