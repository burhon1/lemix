from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import Group

from user.models import CustomUser

def employees_view(request):
    context = {}
    if request.method == "POST":
        post = request.POST
        first_name = post.get('first_name',False)
        last_name = post.get('last_name',False)
        phone = post.get('phone',False)
        birtday = post.get('birtday',False)
        gender = post.get('gender',False)
        location = post.get('location',False)
        groups = post.getlist('groups',False)
        if first_name and last_name and phone and birtday and gender and location and groups:
            custom_user = CustomUser.objects.create(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                birtday=birtday,
                gender=gender,
                location=location,
                password=phone
            )
            custom_user.save()
            groups = Group.objects.filter(id__in=groups)
            custom_user.groups.add(*groups)
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