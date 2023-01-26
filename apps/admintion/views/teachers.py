from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from admintion.models import Teacher, EduCenters
from admintion.services.teacher import update_teacher
from user.services.users import user_add
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse

@permission_required('admintion.teacher_view')
def teachers_view(request):
    context = {}
    if request.method == "POST":
        post = request.POST
        groups = Group.objects.filter(name="Teacher")
        educenter = post.get('educenter',False)
        status,obj = user_add(groups,post, True).values()
        teacer_type=post.get('teacer_type',False)
        status_ = post.get('status',False)
        if status==200 and teacer_type and status_:
            teacher = Teacher(
                teacer_type=teacer_type,
                user=obj,
                status=status_
            )
            if educenter:
                teacher.educenter=EduCenters.objects.filter(id=educenter).first()
            teacher.save()
            return redirect('admintion:teachers')
        else:
            context['error'] = 'Malumotlar to\'liq kiritilmadi'  
            return redirect(reverse('admintion:teachers')+f"?error={context['error']}")
    ed_id=request.user.educenter
    educenter_ids = EduCenters.objects.filter(id=ed_id).values_list('id',flat=True)|EduCenters.objects.filter(parent__id=ed_id).values_list('id',flat=True)              
    teacher = Teacher.teachers.teachers(educenter_ids) 
    context['objs'] = teacher
    context['educenters'] = EduCenters.objects.filter(id=ed_id).values('id','name')|EduCenters.objects.filter(parent__id=ed_id).values('id','name')
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