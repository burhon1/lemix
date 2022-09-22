from django.shortcuts import render,redirect
from django.urls import reverse
from user.services.users import user_add
from django.contrib.auth.models import Group
from admintion.models import Student

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
    context['students'] = Student.objects.all()
    print(context['students'])
    print(Student.students.students())
    return render(request,'admintion/students.html',context) 


def student_detail_view(request,id):
    context = {}
    if request.method == "POST":
        post = request.POST
    return render(request,'admintion/student_detail.html',context)