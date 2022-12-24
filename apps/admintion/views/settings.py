from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required

from admintion.models import EduCenters
from user.models import UserDevices
from admintion.forms.settings import EduCentersForm


@permission_required('admintion.view_educenters')
def settings_view(request):
    context = {
        'sessions': UserDevices.devices.filter(user=request.user)
    }
    if request.user.groups.filter(name='Direktor').exists():
        educenter = EduCenters.objects.filter(director=request.user).first()
    else:
        educenter = request.user.educenter
    
    if request.method == 'POST' and request.user.has_perm('admintion.change_educenters'):
        form = EduCentersForm(request.POST, request.FILES, instance=educenter)
        print(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('admintion:settings'))
        else:
            print(form.errors)
    else:
        form = EduCentersForm(instance=educenter)
    context['educenter'] = educenter
    context['form'] = form
    return render(request, 'admintion/umumiy_sozlamalar.html', context)