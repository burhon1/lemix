from django.shortcuts import render, get_object_or_404, redirect
from django.forms.models import model_to_dict
from django.db.models import Q
from django.contrib.auth.models import Group
from django.urls import reverse
from django.contrib import messages 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from admintion.models import LeadForms,Course,Sources,FormLead,FormUniversalFields,FormFields,EduCenters,Contacts, LeadStatus
from admintion.forms.leads import LeadFormClass,LeadSaveFormClass,FieldsFormSet,ContactsFormSet,LeadFormRegisterForm
from admintion.services.qrcode import create_qrcode
from user.services.users import user_add

@login_required
def forms_view(request):
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter = EduCenters.objects.filter(qury)
    if request.method == 'POST':
        form = LeadSaveFormClass(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            educenters = request.POST.get('educenters',False)
            sources = request.POST.get('sources',False)
            courses = request.POST.get('courses',False)
            # obj.save()
            if educenters:
                # obj.educenters.add(EduCenters.objects.filter(id=educenter).first())
                obj.educenters = EduCenters.objects.filter(id=educenters).first()
            elif int(ed_id) != 0:
                obj.educenters=educenter.first()     
            if sources:
                # obj.sources.add(Sources.objects.filter(id=sources).first()) 
                obj.sources=Sources.objects.filter(id=sources).first() 
            if courses:
                # obj.courses.add(Course.objects.filter(id=courses).first())   
                obj.courses = Course.objects.filter(id=courses).first()       
            
            obj.save()
            data = request.build_absolute_uri(reverse('lead_registration_view', args=[obj.id]))+'?title='+obj.title
            create_qrcode(data, obj)
            return JsonResponse({'id': obj.id}, status=201)
        else:
            errors = dict(form.errors.items())
            print(errors)
            return JsonResponse(errors, status=400, safe=False)
    educenter_ids = educenter.values_list('id',flat=True)
    context = {
        'objs':LeadForms.lead_forms.lead_forms(educenter_ids),
        'form': LeadFormClass(),
    }       
    return render(request,'admintion/forms.html',context) 

@login_required
def form_delete_view(request, pk):
    instance = get_object_or_404(LeadForms, pk=pk)
    instance.delete()
    message = "O'chirildi"
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
        post = request.POST
        name=post.get('name',False)
        title=post.get('title',False)
        comment=post.get('comment',False)
        educenters=post.get('educenters',False)
        courses=int(post.get('courses',False))
        sources=int(post.get('sources',False))
        if name and title:
            instance.title=title
            instance.name=name
            if comment:
                instance.comment=comment
            if educenters:
                instance.educenters=EduCenters.objects.get(id=educenters)
            elif educenters == 0:
                instance.educenters=None  
            if courses:
                instance.courses=Course.objects.get(id=courses)
            elif courses == 0:
                instance.courses=None
            if sources:
                instance.sources=Sources.objects.get(id=sources) 
            elif sources == 0:
                instance.sources=None     
            instance.save()
            return JsonResponse({'id': instance.id}, status=200)
        else:      
            return JsonResponse('', status=400, safe=False)            
        # if 
        # if form.is_valid():
        #     print(form)
        #     obj = form.save()
        #     return JsonResponse({'id': obj.id}, status=200)
        # else:
        #     errors = dict(form.errors.items())
        #     return JsonResponse(errors, status=400, safe=False)
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
    if instance.educenters is None:
        context['obj'].update({'educenters':""})
    else:
        context['obj'].update({'educenters':instance.educenters.id})
    if instance.courses is None:
        context['obj'].update({'courses':""})
    else:
        context['obj'].update({'courses':instance.courses.id})
    if instance.sources is None:
        context['obj'].update({'sources':""})
    else:
        context['obj'].update({'sources':instance.sources.id})

    
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
    is_seen = request.session.get('is_seen',False)

    if not(is_seen):
        request.session['is_seen']=1
        leadform.seen += 1
        leadform.save(update_fields=['seen'])
    form = LeadFormRegisterForm(form=leadform)

    context = {'pk':pk, 'title':leadform.title, 'main_edu': '', 'educenters':leadform.educenters, 'form':form}
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
        context['edu_count'] =  0    
    return render(request, "admintion/lead_form.html", context=context)

def lead_registration2_view(request, pk):
    context={}
    leadform = get_object_or_404(LeadForms, pk=pk)
    if request.method == "POST":
        post = request.POST
        data = {}
        if leadform.educenters is None:
            data['educenter'] = EduCenters.objects.get(id=post.get('educenters'))
        else:
            data['educenter']= leadform.educenters
        if  leadform.courses is None:  
            data['course']=Course.objects.get(id=post.get('courses'))   
        else:
            data['course']= leadform.courses    
        if leadform.sources is None:
            data['source'] = Sources.objects.get(id=post.get('sources'))  
        else:
            data['source']= leadform.sources 
        phone_number=post.get('phone',False)
        fio=post.get('fio',False) 
        data['status'],_ = LeadStatus.objects.get_or_create(status='Telefon qilish',color='danger')
        groups = Group.objects.filter(name="Lead")
        status,obj = user_add(groups,request,True).values()
        # for field in fields:
        #     data['source']=
        if phone_number and fio and status==200:
            data['user']=obj
            data['via_form']=leadform
            form_lead = FormLead(**data)
            form_lead.save()
            # context['first_name'] = fname if fname else ""
            # context['last_name'] = lname if lname else ""
            return render(request, "admintion/lead_form_success.html", context)
    # print(request.session['is_seen'])
    is_seen = request.session.get(str(leadform.id)+'_seen',False)
    
    if not(is_seen):
        request.session[str(leadform.id)+'_seen']=leadform.id
        leadform.seen += 1
        leadform.save(update_fields=['seen'])
    fields=leadform.formfields_set.all().order_by('order')
    context['objs'] = leadform
    context['fields'] = fields
    if leadform.educenters is None:
        context['educenters'] = EduCenters.objects.all().values('id','name')
    if (leadform.educenters is not None) and (leadform.courses is None):  
        context['courses']=Course.objects.filter(educenter=leadform.educenters).values('id','title')
    if leadform.sources is None:
        context['sources'] = Sources.objects.all().values('id','title')    

    return render(request, "admintion/lead_form2.html",context=context)


