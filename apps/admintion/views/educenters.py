from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from admintion.models import EduCenters, Regions, Districts
from admintion.forms.educenters import EducentersForm
from django.db.models import Q

@permission_required('admintion.view_educenters')
def educenters_view(request):
    ed_id=request.session.get('branch_id',False)
    # qury = Q(id=ed_id)
    # if int(ed_id) == 0:
    #     qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenters = EduCenters.objects.filter(parent__id=request.user.educenter)
    if request.method == 'POST':
        form = EducentersForm(request.POST)
        if form.is_valid():
            form.save(request.user.educenter)
            return redirect(reverse('admintion:edu-centers')+"?status=ok")
    form = EducentersForm()
  
    context = {
        'objects': educenters,
        'form': form,
    }
    return render(request, 'admintion/filiallar.html', context=context)

@permission_required('admintion.view_educenters')
def educenter_detail(request, pk):
    educenter = EduCenters.educenters.educenter(pk)
    return JsonResponse(educenter, safe=False)

@permission_required('admintion.change_educenters')
def educenter_update_view(request, pk):
    obj = get_object_or_404(EduCenters, pk=pk)
    form = EducentersForm(request.POST, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
    else:
        messages.add_message(request, messages.WARNING, "Bajarilmadi. Iltimos ma'lumotlar to'laqonli kiritilganiga ahamiyat bering.")
    return redirect(reverse('admintion:edu-centers')+"?status=ok")

@permission_required('admintion.delete_educenters')
def educenter_delete_view(request, pk):
    obj = get_object_or_404(EduCenters, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect(reverse('admintion:edu-centers')+"?status=ok")


def connected_regs(request):
    pk: int = request.GET.get('c', None)
    reg_pk: int = request.GET.get('r', None)
    filters = {'country_id': pk}
    
    regions = Regions.objects.filter(**filters).values('id', 'name')
    if reg_pk:
        filters['region_id'] =  reg_pk 
    districts = Districts.objects.filter(**filters).values('id', 'name')
    data = {
        'regions': list(regions), 'districts': list(districts)
    }
    return JsonResponse(data, safe=False)