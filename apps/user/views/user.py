from django.http import JsonResponse
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from user.forms import UserForm
from user.models import CustomUser

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