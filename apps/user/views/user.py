import random
from django.http import JsonResponse
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from user.forms import UserForm, ChangePasswordForm
from user.models import CustomUser
from admintion.services.send_sms import send_message
from admintion.services.sms import get_sms_integration
from django.contrib import messages
def user_create_view(request):
    form = UserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            return JsonResponse(model_to_dict(user, fields=('id', 'phone',)))
        else:
            return JsonResponse(form.errors, safe=False, status=400)
    return JsonResponse(['method is not POST'], safe=False, status=400)

def user_update_view(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                return JsonResponse({'message': f"{request.POST.get('phone')} telefon raqamidan foydalanilgan."})
            return JsonResponse(model_to_dict(user, fields=('id', 'phone',)))
        else:
            return JsonResponse(form.errors, safe=False, status=400)
    return JsonResponse(['method is not POST'], safe=False, status=400)

@login_required
def change_password_view(request):
    form = ChangePasswordForm(request.POST, instance=request.user)
    print(request.POST)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, "Parol yangilandi.")
        return redirect(reverse('user:login')+f"?next={reverse('admintion:settings')}")
    else:
        messages.add_message(request, messages.WARNING, "Parol mos emas. Qaytadan kiriting")
        return redirect(reverse('admintion:settings')+"?error=Parol mos emas. Qaytadan kiriting")
    


@login_required
def gen_otp(request):
    otp = random.randint(142099, 891079)
    request.user.otp=otp
    request.user.save()
    print(otp)
    sms_in = get_sms_integration(main=True)
    email, password = sms_in.email, sms_in.password
    message = f"Sizning vaqtinchalik parolingiz: {otp}.\n Uni hech kimga bermang."
    status = send_message(request.user.phone, message, email, password,request)
    
    if status == 201:
        return JsonResponse({'message':'Xabar yuborildi', 'phone':request.user.phone}, status=201)
    elif status==503:
        return JsonResponse({'message':'Xatolik sodir bo\'ldi.Iltimos keyinroq urinib ko\'ring', 'phone':''}, status=503)
