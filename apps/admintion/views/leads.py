from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from admintion.forms.leads import LeadForm, DemoForm, DemoFormset
from admintion.utils import convert_to_json
from admintion.models import Course, FormLead, Group, GroupStudents, GroupsDays, LeadDemo, LeadStatus, TaskTypes, Tasks, Student,Sources
from admintion.selectors import get_form_leads, get_demos, get_lead_tasks, get_next_lesson_date, select_groups_by_limit
from admintion.data.chooses import GET_GROUPS_DAYS, STUDENT_SOURCES
from user.models import CustomUser

def leads_view(request):
    template_name = 'admintion/lidlar_royxati.html'
    activity = int(request.GET.get('status', 1))
    if  activity == 2:
        template_name = 'admintion/lidlar_arxiv.html' 
    context = dict()
    context['leads'] = get_form_leads({'activity':activity}, (
        'id', 'user__first_name', 'user__last_name', 'user__phone', 'status__status', 'comment', 'source', 'author', 'author__first_name', 'author__last_name', 'created_at', 'modified_at', 'via_form__title'))
    
    # context['sources'] = Sources.objects.all() #[ {'id':key, 'source':value} for key, value in dict(STUDENT_SOURCES).items()]
    context['lead_statuses'] = LeadStatus.objects.values('id', 'status')
    context['courses'] = Course.objects.filter(status=True).values('id', 'title')
    groups = Group.objects.filter(status__in=[2, 3, 4]).values('id', 'title', 'course__title')
    context['groups'] = select_groups_by_limit(groups)
    context['task_types'] = TaskTypes.objects.values('id', 'task_type')
    context['days'] = GroupsDays.objects.values('id', 'days')
    context['task_responsibles'] = CustomUser.objects.filter(Q(is_superuser=True)|Q(is_staff=True)).values('id', 'first_name', 'last_name')
    for day in context['days']:
        day['day_name'] = dict(GET_GROUPS_DAYS)[day['days']]
    return render(request,template_name, context)

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
            print(form.errors)
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
    groups = Group.objects.filter(status__in=[2, 3, 4]).values('id', 'title', 'course__title')
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