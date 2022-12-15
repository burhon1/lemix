from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

from admintion.models import EduCenters
from user.models import UserDevices

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
        if request.POST.get('oferta'):
            educenter.oferta = request.FILES.get('oferta')
        if request.POST.get('s_contract'):
            educenter.s_contract = request.FILES.get('s_contract')
        if request.POST.get('j_contract'):
            educenter.j_contract = request.FILES.get('j_contract')
        if request.POST.get('t_contract'):
            educenter.t_contract = request.FILES.get('t_contract')
        educenter.save()
    context['educenter'] = educenter
    print(context)
    return render(request, 'admintion/umumiy_sozlamalar.html', context)