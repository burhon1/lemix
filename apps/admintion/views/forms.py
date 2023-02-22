from django.shortcuts import render, get_object_or_404, redirect
from django.forms.models import model_to_dict
from django.urls import reverse
from django.contrib import messages 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from admintion.models import LeadForms,FormUniversalFields,FormFields,EduCenters,Contacts, LeadStatus
from admintion.forms.leads import LeadFormClass,FieldsFormSet,ContactsFormSet,LeadFormRegisterForm
from admintion.services.qrcode import create_qrcode

@login_required
def forms_view(request):
    if request.method == 'POST':
        form = LeadFormClass(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            # obj.ed
            obj.save()
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
            contacts = leadform.contacts_set.all()
            for form in formset:
                value = form.cleaned_data.get('value')
                content_type = form.cleaned_data.get('contact_type')
                contact = contacts.filter(contact_type=content_type).first()
                if contact:
                    contact.value = value
                    contact.save()
                else:
                    contact = Contacts.objects.create(value=value, contact_type=content_type, leadform=leadform)
            return JsonResponse({}, status=201)
        else:
            errors = dict(formset.errors)
            return JsonResponse(errors, status=400, safe=False)
    form_fields = leadform.contacts_set.all().values('id','value','contact_type',)
    form_fields = list(form_fields)
    return JsonResponse(form_fields, safe=False)
 

def contacts_delete_view(request, pk):
    leadform = get_object_or_404(LeadForms, pk=pk)
    if request.method=='POST':
        contacts = request.POST.getlist('contacts')
        contacts = [int(contact) for contact in contacts if contact.isnumeric()]
        print("contacts", contacts)
        leadform.contacts_set.filter(id__in=contacts).delete()
        return JsonResponse({}, status=204)
    return JsonResponse({}, status=200)

def lead_registration_view(request, pk):
    leadform = get_object_or_404(LeadForms, pk=pk)
    leadform.seen += 1
    leadform.save(update_fields=['seen'])
    form = LeadFormRegisterForm(form=leadform)
    context = {'pk':pk, 'title':leadform.title, 'main_edu': (leadform.educenters.filter(parent=None) or EduCenters.objects.filter(parent=None)).first(), 'educenters':leadform.educenters.all(), 'form':form}
    context['contacts'] = leadform.contacts_set.all()
    if request.method == "POST":
        form = LeadFormRegisterForm(leadform, request.POST, request.FILES)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.status = LeadStatus.objects.first()
            lead.save()
            
            fname = lead.user.first_name or ""
            lname = lead.user.last_name or ""
            context['first_name'] = fname if fname else ""
            context['last_name'] = lname if lname else ""
            return render(request, "admintion/lead_form_success.html", context)
        else:
            messages.add_message(request, messages.WARNING, 'Bu raqam oldin ro\'yxatdan o\'tgan.')
            return redirect(reverse('lead_registration_view', args=[pk])+f"?title={request.GET.get('title', '')}")
    else:
        context['edu_count'] = len(context['educenters'])     
    return render(request, "admintion/lead_form.html", context=context)


