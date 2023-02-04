from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.services.users import add_to_device_list
from ..models import CustomUser, UserDevices

def login_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('user:account')
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
                    next = request.GET.get('next')
                    if next:
                        return redirect(reverse('user:account')+f'?next={next}')
                    group = user.first().groups.values_list('name',flat=True)
                    if len(group)!=0:
                        next = request.GET.get('next', None)
                        if next:
                            return redirect(next)
                        if 'Admintion' in group:
                            return redirect('admintion:courses')
                        elif 'Teacher' in group or 'Direktor' in group:
                            return redirect('admintion:dashboard')
                        elif 'Student' in group:
                            return redirect('student:student')   
                    return redirect('user:login')  
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
    