from django.shortcuts import render,redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from admintion.models import LeadForms,FormUniversalFields,FormFields,EduCenters
from admintion.forms.leads import LeadFormClass,FieldsFormSet,ContactsFormSet,LeadFormRegisterForm
from admintion.services.qrcode import create_qrcode

@login_required
def forms_view(request):
    if request.method == 'POST':
        form = LeadFormClass(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            data = request.build_absolute_uri(reverse('lead_registration_view', args=[obj.id]))+'?title='+obj.title
            create_qrcode(data, obj)
            return JsonResponse({'id': obj.id}, status=201)
        else:
            errors = dict(form.errors.items())
            return JsonResponse(errors, status=400, safe=False)
    context = {
        'objs': LeadForms.objects.all().order_by('-id'),
        'form': LeadFormClass(),
    }         
    return render(request,'admintion/forms.html',context) 

@login_required
def form_delete_view(request, pk):
    instance = get_object_or_404(LeadForms, pk=pk)
    if len(instance.sources.all()):
        instance.delete()
        message = "O'chirildi"
    else:
        message = f"Bu forma manbaaga bog'langan. Uni o'chirish uchun manbani o'chirishingiz kerak."
    return JsonResponse({'message':message}, status=204)

@login_required
def form_detail_view(request, pk):
    instance = get_object_or_404(LeadForms, pk=pk)
    data = {
        'link':request.build_absolute_uri(reverse('lead_registration_view', args=[instance.id]))+'?title='+instance.title
    }
    if instance.qrcode:
        data['image'] = instance.qrcode.url
    return JsonResponse(data)


@login_required
def form_update_view(request, pk):
    instance = get_object_or_404(LeadForms, pk=pk)
    if request.method == 'POST':
        form = LeadFormClass(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({'id': obj.id}, status=200)
        else:
            errors = dict(form.errors.items())
            return JsonResponse(errors, status=400, safe=False)
    context = {
        'obj':model_to_dict(instance, fields=('id', 'title','name','comment','russian','english')),
        'fields': instance.formfields_set.all().values('id','key','order','required','title'),
        'contacts': instance.contacts_set.all().values('id','contact_type','value')
    }
    context['fields'] = list(context['fields'])
    context['contacts'] = list(context['contacts'])

    if instance.image:
        context['obj'].update({'image':{
            'name': instance.image.name,
            'url': instance.image.url
        }})
    if len(instance.educenters.all())>1:
        context['obj'].update({'educenters':""})
    else:
        context['obj'].update({'educenters':instance.educenters.first().id})
    if len(instance.courses.all())>1:
        context['obj'].update({'courses':""})
    else:
        context['obj'].update({'courses':instance.courses.first().id})
    if len(instance.sources.all())>1:
        context['obj'].update({'sources':""})
    else:
        context['obj'].update({'sources':instance.sources.first().id})
    
    return JsonResponse(context, status=200)

def universal_fields_view(request):
    if request.method == 'POST':
        title = request.POST.get('title', None)
        if title:
            uni_fields = [obj.title for obj in FormUniversalFields.objects.all()]
            if title in uni_fields:
                i = 1
                while f"{title} {i}" in uni_fields:
                    i+=1
                title=f"{title} {i}"
            FormUniversalFields.objects.create(title=title)
            status = 201
        else:
            status = 400
        return JsonResponse({}, status=status)
    context = {
        'objs': list(FormUniversalFields.objects.all().values('id','title','key','required','order'))
    }
    return JsonResponse(context, safe=False)

@login_required
def form_fields_view(request, pk):
    leadform = get_object_or_404(LeadForms, pk=pk)
    if request.method == 'POST':
        formset = FieldsFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                obj = form.save(commit=False)
                obj.leadform = leadform
                obj.save()
            return JsonResponse({}, status=201)
        else:
            errors = dict(formset.errors.items())
            return JsonResponse(errors, status=400, safe=False)
    form_fields = FormFields.objects.filter(leadform=leadform).values('id','title','key','required','order')
    form_fields = list(form_fields)
    return JsonResponse(form_fields, safe=False)

@login_required
def form_fields_delete_view(request, pk):
    leadform = get_object_or_404(LeadForms, pk=pk)
    if request.method == 'POST':
        ids = request.POST.getlist('ids')
        ids = [int(id) for id in ids if type(id)== str and id.isnumeric()]
        fields = leadform.formfields_set.filter(id__in=ids).delete()
        return JsonResponse({}, status=204)
    return JsonResponse({}, status=400)

@login_required
def contacts_view(request, pk):
    leadform = get_object_or_404(LeadForms, pk=pk)
    if request.method == 'POST':
        formset = ContactsFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                obj = form.save(commit=False)
                obj.leadform = leadform
                obj.save()
            return JsonResponse({}, status=201)
        else:
            print(formset.errors)
            errors = dict(formset.errors)
            return JsonResponse(errors, status=400, safe=False)
    form_fields = leadform.contacts_set.all().values('id','value','contact_type',)
    form_fields = list(form_fields)
    return JsonResponse(form_fields, safe=False)
 

def lead_registration_view(request, pk):
    leadform = get_object_or_404(LeadForms, pk=pk)
    template_name = "admintion/lead_form.html"
    form = LeadFormRegisterForm(form=leadform)
    context = {'pk':pk, 'main_edu': (leadform.educenters.filter(parent=None) or EduCenters.objects.filter(parent=None)).first(), 'educenters':leadform.educenters.all(), 'form':form}
    get = request.GET
    if request.method == "POST":
        form = LeadFormRegisterForm(leadform, request.POST, request.FILES)
        if form.is_valid():
            form.clean()
            lead = form.save()
            # print(form)
            template_name = "admintion/lead_form_success.html"
            context['first_name'] = lead.user.first_name
            context['last_name'] = lead.user.last_name
    else:
        context['edu_count'] = len(context['educenters'])
    context['contacts'] = leadform.contacts_set.all()
    request.GET['title'] = leadform.title
    return render(request, template_name, context=context)


