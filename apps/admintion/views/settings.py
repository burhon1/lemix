from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from admintion.models import EduCenters
from user.models import UserDevices
from admintion.forms.settings import EduCentersForm


@permission_required('admintion.view_educenters')
def settings_view(request):
    context = {
        'sessions': UserDevices.devices.filter(user=request.user)
    }
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter = EduCenters.objects.filter(qury).first()
    if request.method == 'POST' and request.user.has_perm('admintion.change_educenters'):
        form = EduCentersForm(request.POST, request.FILES, instance=educenter)
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