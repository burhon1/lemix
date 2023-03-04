from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from getmac import get_mac_address
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from admintion.models import EduCenters,Sources,LeadForms,Course
from admintion.services.qrcode import create_qrcode
from user.services.users import get_client_ip
from user.models import UserDevices
from admintion.forms.settings import EduCentersForm


@permission_required('admintion.view_educenters')
def settings_view(request):
    ip = get_client_ip(request)
    mac_address = get_mac_address(ip=ip, network_request=True)
    context = {
        'sessions': UserDevices.devices.filter(user=request.user).exclude(mac_address=mac_address)
    }
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter = EduCenters.objects.filter(qury).first()
    if request.method == 'POST' and request.user.has_perm('admintion.change_educenters'):
        name  = request.POST.get('name',False)
        if name:
            educenter.name=name
        phone_number  = request.POST.get('phone_number',False)
        if phone_number:
            educenter.phone_number=phone_number 
        teacher_can_see_payments  = request.POST.get('teacher_can_see_payments',False)
        if teacher_can_see_payments:
            educenter.teacher_can_see_payments=teacher_can_see_payments 
        teacher_can_sign_contracts  = request.POST.get('teacher_can_sign_contracts',False)
        if teacher_can_sign_contracts:
            educenter.teacher_can_sign_contracts=teacher_can_sign_contracts            
        # phone =
        # logo = 
        # oferta = 
        # s_contract =
        # t_contract =
        # j_contract =
        # teacher_can_see_payments =
        # teacher_can_sign_contracts =  
        educenter.save()
        return redirect(reverse('admintion:settings'))
        
    else:
        form = EduCentersForm(instance=educenter)
    context['educenter'] = educenter
    context['form'] = form
    context['sources'] = Sources.objects.all()
    return render(request, 'admintion/umumiy_sozlamalar.html', context)


def sources_view(request):
    if request.method == "POST":
        title = request.POST.get('source',False)
        if title:
            source = Sources(title=title)
            source.save()
            lead_form = LeadForms(
                name=source.title,
                title="Ro'yxatdan o'tish"
            )
            lead_form.save()
            lead_form.sources.add(source)
            educe_center = EduCenters.objects.all()
            course = Course.objects.all()
            lead_form.educenters.add(*educe_center)
            lead_form.courses.add(*course)
            data = request.build_absolute_uri(reverse('lead_registration_view', args=[lead_form.id]))+'?title='+lead_form.title
            create_qrcode(data, lead_form)
        return JsonResponse({})
    return redirect('admintion:settings')