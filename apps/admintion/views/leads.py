from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from admintion.forms.leads import LeadForm, DemoForm, DemoFormset
from admintion.utils import convert_to_json
from admintion.models import Course, FormLead, Group as GroupModel, GroupStudents, GroupsDays, EduCenters, LeadStatus, TaskTypes, Tasks, Student,Sources
from admintion.selectors import get_form_leads, get_demos, get_lead_tasks, get_next_lesson_date, select_groups_by_limit
from admintion.data.chooses import GET_GROUPS_DAYS, STUDENT_SOURCES
from admintion.utils import get_list_of_filter
from user.services.users import user_add
from user.models import CustomUser

def leads_view(request):
    context = dict()
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter = EduCenters.objects.filter(qury)
    if request.method=="POST":
        post = request.POST
        if educenter.count() == 1:
            p_phone=post.get("phone",False)
            source=post.get("manba",False)
            status=post.get("hol",False)
            comment=post.get("description",False)
            parent=post.get("parent_name",False)
            parent_phone=post.get("parent_phone",False)
            groups = Group.objects.filter(name="Lead")
            telegram = post.get('telegram_telegram',None)
            passport = post.get('passport_passport', None)
            location = post.get('location_location', None)
            email = post.get('email_location', None)
            file = request.FILES.get('file_file',None)
            status,obj = user_add(groups,request,True).values()
            if status==200:
                source = Sources.objects.filter(id=source).first()
                status = LeadStatus.objects.filter(id=status).first()
                form_lead = FormLead(
                    user=obj,
                    source=source,
                    p_phone=p_phone,
                    status=status,
                    educenter=educenter.first()
                )
                form_lead.telegram=telegram
                form_lead.passport=passport
                # form_lead.file=file
                if comment:
                    form_lead.comment=comment
                if parent and parent_phone:
                    parent_user,created = CustomUser.objects.get_or_create(phone=parent_phone)
                    parent_user.first_name = parent
                    if parent_user.password == '':
                        parent_user.set_password(parent_phone)
                    form_lead.parents=parent_user    
                form_lead.save()  
                return redirect(reverse('admintion:lead-list'))
        return redirect(reverse('admintion:lead-list')+f"?error=Filyalni tanlang")        
    educenter_ids=educenter.values_list('id',flat=True)
    context['objs'] = FormLead.leads.leads(educenter_ids)
    context['sources'] = Sources.objects.all() 
    context['lead_statuses'] = LeadStatus.objects.filter().values('id', 'status')
    context['groups'] = GroupModel.groups.group_list(educenter_ids)
    context['task_types'] = TaskTypes.objects.values('id', 'task_type')
    context['task_responsibles'] = CustomUser.objects.filter(Q(is_superuser=True)|Q(is_staff=True)).values('id', 'first_name', 'last_name')
    context['keys'] = ['check',
            'full_name',
            'phone_number',
            'source__title',
            'status__status',
            'comment',
            'author_name',
            'via_form__title',
            'created_at','action']
    return render(request,"admintion/lidlar_royxati.html", context)

def leads_filter_view(request):
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter_ids = EduCenters.objects.filter(qury).values_list('id',flat=True)   

    status = request.GET
    filter_keys=get_list_of_filter(status)

    leads = list(FormLead.leads.leads_filter(filter_keys,educenter_ids))
    
    return JsonResponse({'data':leads,'status':200})

def leads_archive_view(request):
    context={}
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter = EduCenters.objects.filter(qury)
    educenter_ids=educenter.values_list('id',flat=True)
    context['objs'] = FormLead.leads.leads(educenter_ids,2)
    context['sources'] = Sources.objects.all() 
    context['lead_statuses'] = LeadStatus.objects.filter().values('id', 'status')
    context['groups'] = GroupModel.groups.group_list(educenter_ids)
    context['task_types'] = TaskTypes.objects.values('id', 'task_type')
    context['task_responsibles'] = CustomUser.objects.filter(Q(is_superuser=True)|Q(is_staff=True)).values('id', 'first_name', 'last_name')
    context['keys'] = ['check',
            'full_name',
            'phone_number',
            'source__title',
            'status__status',
            'comment',
            'author_name',
            'via_form__title',
            'created_at','action']
    return render(request,"admintion/lidlar_arxiv.html", context)

def lead_create_view(request):
    if request.method == 'POST':
        form = LeadForm(request.POST, request.FILES)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.author = request.user
            lead.save()
            form.save_m2m()
            lead_data = convert_to_json(lead, fields=('id', 'user', 'source_id', 'comment'))
            return JsonResponse(lead_data, status=201)
        else:
            return JsonResponse({'message': 'error occured'}, safe=False, status=400)
    return JsonResponse({'method':'get'}, status=400)


def lead_detail_view(request, pk):
    lead = get_object_or_404(FormLead, pk=pk)
    context = dict()
    context['lead'] = lead
    context['demos'] = get_demos(lead)
    context['lead_statuses'] = LeadStatus.objects.values('id', 'status')
    context['tasks'] = get_lead_tasks(lead)
    context['courses'] = Course.objects.filter(status=True).values('id', 'title')
    groups = GroupModel.objects.filter(status__in=[2, 3, 4]).values('id', 'title', 'course__title')
    context['groups'] = select_groups_by_limit(groups)
    context['today_tasks'] = []
    temp = []
    for task in context['tasks']:
        if task['deadline'].date() == timezone.now().date():
            context['today_tasks'].append(task)
            temp.append(task['id'])
    context['tasks'] = [ task for task in context['tasks'] if task['id'] not in temp]
    context['count'] = {'tasks': len(context['tasks'])+len(context['today_tasks']), 'today_tasks': len(context['today_tasks'])}
    context['sources'] = Sources.objects.all()#[ {'id':key, 'source':value} for key, value in dict(STUDENT_SOURCES).items()]
    context['days'] = GroupsDays.objects.values('id', 'days')
    context['task_responsibles'] = CustomUser.objects.filter(Q(is_superuser=True)|Q(is_staff=True)).values('id', 'first_name', 'last_name')
    context['task_types'] = TaskTypes.objects.all().values('id', 'task_type')
    for day in context['days']:
        day['day_name'] = dict(GET_GROUPS_DAYS)[day['days']]
        day['selected'] = lead.days.filter(id__in=[int(day['id'])]).exists()
    return render(request, 'admintion/lidlar_edit.html', context)

@login_required
def lead_edit_view(request, pk):
    lead = get_object_or_404(FormLead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, request.FILES, instance=lead)
        if form.is_valid():
            lead_user = lead.user
            lead = form.save(commit=False)
            lead.days.set(form.cleaned_data.get('days', lead.days.all()))
            lead.author = getattr(lead, 'author') or request.user
            lead.user = lead_user
            lead.save()
            data = convert_to_json(lead, fields="__all__")
            return JsonResponse(data) 
        else:
            pass
    return JsonResponse({"message":'not updated'}, status=400)

@login_required
def lead_activity_change(request, pk:int, action:str):
    lead = get_object_or_404(FormLead, pk=pk)
    message=None
    if lead.activity == 1 and action=='archive':
        lead.activity = 2
        lead.author = request.user 
        lead.save()
        message = 'muzlatildi'
    elif lead.activity == 2:
        if action == 'activate':
            lead.activity = 1
            lead.save()
            message = 'Aktivlashtirildi'
        elif action == 'delete':
            lead.activity = 3
            lead.save()
            message="O'chirildi"
    elif action == 'delete':
        lead.activity = 3
        lead.save()
        message="O'chirildi"
    else:
        message = "Bajarilmadi"
    return JsonResponse({'message': message})


def add_demo(request):
    formset = DemoFormset(request.POST or None)
    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                form.save() 
            return JsonResponse({"status":"Created"}, status=201)
        else:
            return JsonResponse(formset.errors, safe=False, status=400)
    return JsonResponse({})


@login_required
def addto_group(request, pk):
    lead = get_object_or_404(FormLead, pk=pk)
    group = request.POST.get('group', None)
    if group is None:
        return ''
    student = Student(
        user=lead.user, 
        source=lead.source or 1, 
        comment=lead.comment,
        )
    try:
        student.save()
    except Exception as e:
        raise e
    
    group_student = GroupStudents.objects.create(student=student, group_id=int(group))

    lead.activity = 3
    lead.save()
    return JsonResponse({"status":"ok", "group_student": group_student.id}, status=201)