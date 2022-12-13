from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from admintion.models import Teacher, EduCenters
from admintion.services.teacher import update_teacher
from user.services.users import user_add
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
def teachers_view(request):
    context = {}
    if request.method == "POST":
        post = request.POST
        groups = Group.objects.filter(name="Teacher")
        status,obj = user_add(groups,post, True).values()
        teacer_type=post.get('teacer_type',False)
        status_ = post.get('status',False)
        if status==200 and teacer_type and status_:
            teacher = Teacher(
                teacer_type=teacer_type,
                user=obj,
                status=status_
            )
            teacher.save()
            return redirect('admintion:teachers')
        else:
            context['error'] = 'Malumotlar to\'liq kiritilmadi'  
            return redirect(reverse('admintion:teachers')+f"?error={context['error']}")
    context['objs'] = Teacher.teachers.teachers()
    if request.user.educenter:
        context['educenter'] = request.user.educenter
    else:
        context['educenters'] = EduCenters.objects.all().values('id', 'name')
    return render(request,'admintion/teachers.html',context) 


def teacher_update_view(request, id):
    obj = get_object_or_404(Teacher, pk=id)
    if request.method == 'POST':
        
        post = request.POST
        update_teacher(obj, post)
        return JsonResponse({'obj':Teacher.teachers.teacher(id)}, status=200)
    return JsonResponse({
        'obj':Teacher.teachers.teacher(id), 
        'method':'get', 'message':'Method cannot be get. It must be a post.'})

def teacher_detail_view(request,id):
    context = {'obj':Teacher.teachers.teacher(id)}
    return render(request,'admintion/teacher_detail.html',context) 

@permission_required('admintion.delete_teacher')
def teacher_delete_view(request, id):
    teacher = get_object_or_404(Teacher, pk=id)
    if request.method == 'POST':
        user = teacher.user
        # teacher.delete()
        user.delete()
        status = 204
    else:
        status = 200
    return JsonResponse({}, status=status)