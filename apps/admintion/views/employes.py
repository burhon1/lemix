from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import Group
from user.services.users import user_add

from user.models import CustomUser

def employees_view(request):
    context = {}
    if request.method == "POST":
        post = request.POST
        groups = post.getlist('groups',False)
        groups = Group.objects.filter(id__in=groups)
        status,obj = user_add(groups,post).values()
        if status:
            return redirect('admintion:employees')
        else:
            context['error'] = 'Malumotlar to\'liq kiritilmadi'  
            return redirect(reverse('admintion:employees')+f"?error={context['error']}")    
    context['groups']=Group.objects.values('id','name')   
    context['users']=CustomUser.users.users(request.user.id)
    return render(request,'admintion/employees.html',context) 

def employee_detail_view(request,id):
    context = {}    
    context['obj'] = CustomUser.users.user(id)
    return render(request,'admintion/employe_detail.html',context)   