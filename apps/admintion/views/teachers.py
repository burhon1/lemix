from django.shortcuts import render,redirect
from django.urls import reverse
from admintion.models import Teacher
from user.services.users import user_add
from django.contrib.auth.models import Group

def teachers_view(request):
    context = {}
    if request.method == "POST":
        post = request.POST
        groups = Group.objects.filter(name="Teacher")
        status,obj = user_add(groups,post).values()
        teacer_type=post.get('teacer_type',False)
        if status==200 and teacer_type:
            teacher = Teacher(
                teacer_type=teacer_type,
                user=obj
            )
            teacher.save()
            return redirect('admintion:teachers')
        else:
            context['error'] = 'Malumotlar to\'liq kiritilmadi'  
            return redirect(reverse('admintion:teachers')+f"?error={context['error']}")
    context['objs'] = Teacher.objects.teacher()
    return render(request,'admintion/teachers.html',context) 


def teacher_detail_view(request,id):
    context = {}
    if request.method == "POST":
        post = request.POST
    context['objs'] = Teacher.teachers.teachers()
    print(context['objs'].values('full_name'))
    return render(request,'admintion/teacher_detail.html',context) 