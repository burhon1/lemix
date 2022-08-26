from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

from ..models import CustomUser

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
                    return redirect('user:account')
                else:
                    context['error'] = "Parol xato kiritildi"   
            else:
                context['error']='Bunday foydalanuvchi yoq'    
    return render(request,'user/login.html',context)