from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.services.users import add_to_device_list
from ..models import CustomUser, UserDevices

def login_view(request):
    context = {}
    # if request.user.is_authenticated:
    #     return redirect('user:account')
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        if phone_number=="" or password=="":
            context['error']="Telefon yoki parol kiritilmadi"
        else:
            user = CustomUser.objects.filter(phone=phone_number)
            if user.exists():
                success = user.first().check_password(password)
                if success:
                    login(request,user.first())
                    add_to_device_list(request)
                    if request.user.is_superuser or request.user.is_staff:
                        return redirect('education:onlin')
                    elif request.user.student_set.first():
                        return redirect('student:student')
                    elif request.user.teacher_set.first():
                        return redirect('education:onlin')
                    elif request.user.lead:
                        return redirect('student:lead')
                else:
                    context['error'] = "Parol xato kiritildi"   
            else:
                context['error']='Bunday foydalanuvchi yoq'    
    return render(request,'user/login.html',context)

@login_required
def remove_device_view(request, pk):
    device = get_object_or_404(UserDevices, pk=pk)
    status = 'Bajarilmadi.'
    if request.method == 'POST' and request.user == device.user:
        device.delete()
        status = 'ok'
    return redirect(reverse('admintion:settings')+f'?status={status}')
    