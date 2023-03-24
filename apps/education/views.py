from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from admintion.models import Course, GroupStudents, Teacher, Group, Tasks, UserTaskStatus, TaskTypes, FormLead, LeadDemo,Parents,Group as GroupModel,EduCenters
from admintion.selectors import set_tasks_status
from education.models import FAQ, Lessons, Modules, Contents, Resources
from education.selectors import get_courses, get_groups, get_lesson_contents_data, get_modules, get_modules_data, get_lessons, get_lessons_data, get_courses_data, get_courses_via_hws, get_groups_via_hws, get_students_data, get_contents, get_groups_data,get_leads_data,get_lead_homework_contents
from education.forms import LessonAddForm, ContentForm, FAQFormSet, TextContentForm, FAQForm, ModuleForm, HomeworkActionForm, TaskForm
from education.utils import youtube_link_formatter
from education.services import createVideo
from student.models import Homeworks
from user.models import CustomUser
from user.utils import get_admins
from django.db.models import Q
def test2_view(request):
    return render(request,'education/test.html')     

def teachers_view(request):
    return render(request,'education/teachers.html')

def lid_view(request):
    return render(request,'education/lid.html')

def lid_royhati_view(request):
    return render(request,'education/lidlar_royxati.html')

def lid_arxiv_view(request):
    return render(request,'education/lid.html')  

@login_required
def onlin_view(request):
    context = dict()
    filter_keys = {}
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter = EduCenters.objects.filter(qury)
    educenter_ids=educenter.values_list('id',flat=True)
    if request.user.groups.filter(name='Teacher').exists():
        context['is_teacher'] = True
        context['courses'] = Course.courses.course_contents(educenter_ids,request.user)
        context['groups'] = GroupModel.groups.group_content(educenter_ids,request.user)
    else:
        context['courses'] = Course.courses.course_contents(educenter_ids)
        context['groups'] = GroupModel.groups.group_content(educenter_ids)    
    teacher = Teacher.objects.filter(user=request.user).first()
    # context['courses'] = get_courses(request.user)
    

    # context['courses'] = get_courses_data(context['courses'], teacher=teacher)
    # groups = get_groups(request.user)
    
    # print(context['courses'])
    

    return render(request,'education/onlin.html', context) 

@login_required
def onlin_video_view(request, pk):
    content = get_object_or_404(Contents, pk=pk)
    context = dict()
    context['resources'] = list(content.content_resources.values('id', 'file', 'link'))
    context['faqs'] = list(content.faqs.values('id', 'question', 'answer'))
    context['content'] = model_to_dict(content, fields=('id', 'title', 'video', 'video_link', 'text', 'required'))
    context['action'] = 'tahrirlash'
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            content = form.save(commit=False)
            if 'spotlightr.com' not in content.video_link:
                content.video_link = createVideo(request.scheme, video_url=content.video_link, name=content.title) # youtube_link_formatter(content.video_link)
            content.save()
            form.save_m2m()
            data = model_to_dict(content, fields=('id', 'title', 'video_link', 'text', 'required', 'status'))
            if content.video:
                data['video'] = {'name':content.video.name, 'url': content.video.url}
            if data['video_link'] is None:
                data['video_link'] = ''
            data['redirect_id'] = content.lesson.module.course.id
            data['group'] = request.GET.get('group', None)
            return redirect(reverse('education:onlin_video', args=[pk])+'?status=ok')
        else:
            return JsonResponse({'errors': form.non_field_errors()}, status=400, safe=False)
    return render(request,'education/onlin_video.html', context=context) 

@login_required
def onlin_video_create_view(request, lesson_id):
    if request.method == 'POST':
        group = request.GET.get('group', None)
        if group:
            group = get_object_or_404(GroupModel, pk=group)

        lesson = get_object_or_404(Lessons, id=lesson_id)
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            if content.video_link is None: # content.video is None and 
                return JsonResponse({'message': 'havola yuklashingiz kerak'}, status=400) # Video fayl yoki 
            content.content_type = 1 
            content.lesson = lesson 
            content.author = request.user
            video_url = form.cleaned_data.get('video_link', None)
            if video_url:
                content.video_link =  createVideo(request.scheme, video_url=video_url, name=content.title) # youtube_link_formatter(video_url)
            content.save()
            if group:
                content.groups=group
            elif request.user.is_superuser:
                content.groups=group
            data = model_to_dict(content, fields=('id', 'title'))
            data['redirect_id'] = content.lesson.module.course.id
            data['group'] = request.GET.get('group', None)
            return JsonResponse(data, status=201)
        else:
            return JsonResponse({'message':form.non_field_errors()}, status=400)
    return render(request,'education/onlin_video.html')

@login_required
def onlin_text_view(request, lesson_id):
    lesson = get_object_or_404(Lessons, id=lesson_id)
    if request.method == 'POST':
        form = ContentForm(request.POST)
        group = request.GET.get('group', None)
        if group:
            group = get_object_or_404(Group, pk=group)
        if form.is_valid():
            content = form.save(commit=False)
            content.author = request.user 
            content.content_type = 2
            content.lesson = lesson
            content.save()
            if group:
                content.groups=group
            elif request.user.is_superuser:
                content.groups=group
            context = dict()
            context = model_to_dict(content, fields=('id', 'lesson', 'text', 'required', 'status'))
            context['redirect_id'] = content.lesson.module.course.id
            context['group'] = request.GET.get('group', None)
            return JsonResponse(context)
        else:
            return JsonResponse({'form': form, 'status':400})
    return render(request,'education/onlin_text.html') 


def onlin_text_update_view(request, pk):
    context = dict()
    content = get_object_or_404(Contents, pk=pk)
    context['content'] = content
    context['faqs'] = context['content'].faqs.all().values('id', 'question', 'answer')
    context['resources'] = context['content'].content_resources.all().values('id', 'file', 'link')
    context['content'] = model_to_dict(context['content'], fields=('id', 'title', 'text', 'required'))
    if request.method == 'POST':
        data = request.POST
        form = TextContentForm(data, instance=content)
        if form.is_valid():
            form.save()
        else:
            print(form.non_form_errors())
        context['content']['redirect_id'] = content.lesson.module.course.id
        context['content']['group'] = request.GET.get('group', None)
        return JsonResponse(context['content'], status=200)

    return render(request,'education/onlin_text.html', context) 

def onlin_test_view(request):
    return render(request,'education/onlin_test.html') 


def get_content_data(content):
    context = dict()
    context['content'] = model_to_dict(content, fields=('id', 'title', 'text', 'required'))
    if content.homework:
        context['content']['homework'] = {'name': content.homework.name, 'url': content.homework.url}
    context['action'] = 'tahrirlash'
    return context

@login_required
def onlin_hwork_view(request, pk):
    content = get_object_or_404(Contents, pk=pk)
    context = dict()
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            content = form.save()
            context = get_content_data(content)
            context['redirect_id'] = content.lesson.module.course.id
            return JsonResponse(context, status=200)
        else:
            print(form.non_field_errors())
    context = get_content_data(content)
    return render(request,'education/onlin_hwork.html', context) 

@login_required
def onlin_hwork_create_view(request, lesson_id):
    lesson = get_object_or_404(Lessons, id=lesson_id)
    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            content = form.save(commit=False)
            content.author = request.user 
            content.content_type = 4 # CONTENT_CHOICES
            content.lesson = lesson
            
            try:
                group = request.GET.get('group',None)
                group = Group.objects.get(id=group)
                content.groups=group
            except:
                if request.user in get_admins():
                    content.groups=group
            content.save()
            data = model_to_dict(content, fields=('id', 'lesson', 'text', 'required', 'status'))
            data['redirect_id'] = content.lesson.module.course.id
            data['group'] = request.GET.get('group', None)
            return JsonResponse(data)
        else:
            print(form.non_field_errors())
            return JsonResponse({'form': form, 'status':400})
    return render(request,'education/onlin_hwork.html')



@login_required
def onlin_hwork_delete_view(request, pk):
    content = get_object_or_404(Contents, pk=pk)
    if request.method == 'POST' and (request.user in get_admins() or content.author == request.user):
        id = content.lesson.module.course.id
        content.delete()
        return JsonResponse({'status':"O'chirildi", 'url': f'/education/onlines/{id}/'})
    return JsonResponse({'status':'Bajarilmadi'}, status=400)

@login_required
def onlins_view(request,id):
    course = get_object_or_404(Course, id=id)
    group = request.GET.get('group', None)
    context = dict()
    if group:
        group = get_object_or_404(Group, pk=group)
        context['group'] = get_groups_data([group], teacher=request.user.teacher_set.first())[0]
    context['course'] = get_courses_data([course], teacher=request.user.teacher_set.first())[0]

    if request.user.is_superuser is False and group:
        admins = CustomUser.objects.filter(is_superuser=True)
        admins = list(admins)
        if group.teacher:
            admins.append(group.teacher.user)
        if group.trainer:
            admins.append(group.trainer.user)
    else:
        admins = None

    if request.method == 'POST':
        lesson_id = request.POST.get('lesson')
        if lesson_id:
            context['contents'] = get_lesson_contents_data(lesson_id=lesson_id, user=request.user)
        module_id = request.POST.get('module')
        if module_id:
            filter_kwargs = {'module_id': module_id}
            filter_kwargs.update({'groups__id': group.id}) if group else dict()
            context['lessons'] = get_lessons(course, request.user,**filter_kwargs)
            context['lessons'] = get_lessons_data(context['lessons'])
        return JsonResponse(context)

    context['modules'] = get_modules(course, request.user, group=group)
    module_id = request.GET.get('m', None)
    filter_kwargs = {'groups__id': group.id} if group else dict()
    if module_id:
        filter_kwargs = {'module_id': module_id,}
    context['lessons'] = get_lessons(course, request.user, **filter_kwargs)
    context['lessons'] = get_lessons_data(context['lessons'])
    
    context['modules'] = get_modules_data(context['modules'], group=group, authors=admins)
    return render(request,'education/onlins.html', context)


def onlin_lessons_view(request,id):
    context={}
    from django.contrib.postgres.aggregates import ArrayAgg,JSONBAgg
    from django.contrib.postgres.expressions import ArraySubquery
    from django.db.models.expressions import RawSQL
    from django.db.models.functions import JSONObject as jsonobject
    from django.db.models import F,OuterRef,Count,Case,Value,When
    filter_keys = {}
    filter_keys=Q(course__id=id)&Q(groups__isnull = True)
    lesson_filters = Q(module__id=OuterRef("pk"))&Q(groups__isnull = True)
    content_filters = Q(lesson__id=OuterRef("pk"))&Q(groups__isnull = True)
    group = request.GET.get('group', None)
    flkeys=Q(lessons__groups__isnull=True)
    if group is not None:
        flkeys=Q(lessons__groups__isnull=True) | Q(lessons__groups__id=group)
        filter_keys=Q(course__id=id)|Q(Q(course__id=id)&Q(groups__id=group))
        lesson_filters = Q(Q(module__id=OuterRef("pk")) & Q(groups__isnull = True))|Q(Q(module__id=OuterRef("pk"))&Q(groups__id=group))
        # content_filters=Q(Q(lesson__id=OuterRef("pk")) & Q(groups__isnull = True))|Q(Q(lesson__id=OuterRef("pk"))&Q(groups__id=group))
        content_filters=Q(lesson__id=OuterRef("pk"))|Q(Q(lesson__id=OuterRef("pk"))&Q(groups__id=group))
        # lesson_filters=Q(module__id=OuterRef("pk"))|Q(Q(module__id=OuterRef("pk"))&Q(groups__id=group))
    context['modules'] = Modules.modules.module_list(filter_keys)
    # course = Modules.objects.annotate(data=JSONBAgg(city=F("course__title"), zip=F("course__id"))).values('data','id','title')
    contents_subquery = Contents.objects.filter(content_filters)\
                        .annotate(
                            content_type_name=Case(
                                When(content_type=1,then=Value('Video')),
                                When(content_type=2,then=Value('Maqola')),
                                When(content_type=3,then=Value('Test')),
                                default=Value('Uy vazifasi')
                            ),
                            content_status=Case(
                                When(status=True,then=Value(1)),
                                default=Value(0)
                            )
                        )\
                        .annotate(
                            contents=jsonobject(id=F('id'),title=F("title"), content_type=F("content_type_name"),status=F('content_status'))
                        ).values_list("contents").order_by('order')
    subquery = Lessons.objects.filter(lesson_filters)\
        .values('id','title',content=ArraySubquery(contents_subquery)).order_by('order')\
            .annotate(
                contents=jsonobject(id=F('id'),
                title=F("title"),
                content=F("content"),
                lesson_status=Case(
                                When(status=True,then=Value(1)),
                                default=Value(0)
                            )
            )).values_list("contents")
    context['modules_list'] = list(Modules.objects.filter(flkeys).filter(Q(course__id=id)).annotate(lesson_count=Count('lessons')).filter(lesson_count__gt=0).values('id','title',data=ArraySubquery(subquery)))
    context['course']=Course.courses.course_content(id,group)
    return render(request,'education/online_lesson_detail.html', context) 

@login_required
def online_delete_view(request, id):
    course = get_object_or_404(Course, id=id)
    if course.author == request.user or request.user.is_superuser:
        course.modules.all().delete()
        course.tests_set.all().delete()
        return redirect('education:onlins', kwargs={'id':id}) 
    return JsonResponse({'status':'Sizda bunga ruhsat yo\'q'})


@login_required
def online_update_view(request, type, pk):
    if type == 'course':
        obj = get_object_or_404(Course, pk=pk)
    if type == 'module':
        obj = get_object_or_404(Modules, pk=pk)
    if type == 'lesson':
        obj = get_object_or_404(Lessons, pk=pk)
    context = model_to_dict(obj, fields=('id', 'title', 'comment'))    

    if request.method == 'POST':
        data = request.POST
        obj.title = data['title']
        obj.comment =data['comment']
        obj.save()
        return JsonResponse({'status':'ok'})
    return JsonResponse(context, safe=False)


@login_required
def online_delete2_view(request, type:str, pk: int):
    if request.method == 'POST':
        if type == 'course':
            obj = get_object_or_404(Course, pk=pk)
            obj.modules.all().delete()
        if type == 'module':
            obj = get_object_or_404(Modules, pk=pk)
            obj.delete()
        if type == 'lesson':
            obj = get_object_or_404(Lessons, pk=pk)
            obj.delete()
        if type == 'content':
            obj = get_object_or_404(Contents, pk=pk)
            obj.delete()

        # course = get_object_or_404(Course, id=id)
        # if course.author == request.user or request.user.is_superuser:
        #     course.modules.all().delete()
        #     course.tests_set.all().delete()
        return redirect('education:onlins', id=pk) 
    return JsonResponse({'status':'Sizda bunga ruhsat yo\'q'})


@login_required
def online_activate_view(request, action:str, type: str, pk:int):
    ACTIONS = {'activate':True, 'draft':False}
    if request.method == 'POST':
        if type == 'course':
            obj = get_object_or_404(Course, pk=pk)
            obj.status=not(obj.status)
            obj.save()
            modules = obj.modules.all()
            contents = Contents.objects.filter(lesson__module__in=modules)
            contents.update(status=ACTIONS[action])
        if type == 'module':
            obj = get_object_or_404(Modules, pk=pk)
            contents = Contents.objects.filter(lesson__module=obj)
            contents.update(status=ACTIONS[action])
        if type == 'lesson':
            obj = get_object_or_404(Lessons, pk=pk)
            contents = Contents.objects.filter(lesson=obj)
            contents.update(status=ACTIONS[action])
        if type == 'content':
            objs = Contents.objects.filter(pk=pk)
            objs.update(status=ACTIONS[action])
        return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'get request'})    

@login_required
def modules_view(request):
    if request.method == 'POST':
        group = request.GET.get('group', None)
        if group and group !="":
            group = get_object_or_404(Group, pk=group)
        
        form = ModuleForm(request.POST)
        
        if form.is_valid():
            module = form.save(commit=False)
            module.author=request.user
            

            if group and type(group) == Group:
                module.groups=group
                
            elif request.user.is_superuser:
                module.groups=group
                
            module.save()
            data = model_to_dict(module, fields=('id', 'title'))
            data['status'] = False
            return JsonResponse(data, status=201)
        else:
            return JsonResponse(form.errors(), safe=False, status=400)
    return JsonResponse({'status':'ok'})


@login_required
def course_modules_view(request, pk):
    course = Course.objects.filter(id=pk).first()
    group = request.GET.get('group', None)
    if group:
        group = get_object_or_404(Group, pk=group)
    modules = get_modules(course, request.user, group=group)
    context = dict()
    context['modules'] = list(get_modules_data(modules))
    return JsonResponse(context)


@login_required
def course_lessons_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    context = dict()
    context['lessons'] = get_lessons(course, request.user)
    context['lessons'] = get_lessons_data(context['lessons'])
    return JsonResponse(context)

@login_required
def create_lesson_view(request):
    if request.method == 'POST':
        data = request.POST
        group = request.GET.get('group', None)
        if group:
            group = get_object_or_404(Group, pk=group)
        form = LessonAddForm(data)
        if form.is_valid():
            lesson = form.save(author=request.user)
            if group:
                lesson.groups=group
                lesson.save()
            elif request.user.is_superuser:
                lesson.groups=group
                lesson.save()
            return JsonResponse({'lesson': model_to_dict(lesson, exclude=('groups',)), 'status': 201} )
        
        return JsonResponse({'message': 'Forma to\'g\'ri to\'ldirmadingiz.', 'status':400})
    return JsonResponse({'status': 200})

def courses_list_view(request):
    return render(request,'education/courses_list.html')    
   
def course_detail_view(request,id):
    course = get_object_or_404(Course, id=id)
    context = dict()
    context['course'] = get_courses_data([course], teacher=request.user.teacher_set.first())[0]
    
    return render(request,'education/course_detail.html', context) 

def teacher_detail_view(request,id):
    return render(request,'education/teacher_detail.html') 
    
def group_detail_view(request,id):
    return render(request,'education/group_detail.html') 

def student_detail_view(request,id):
    return render(request,'education/student_detail.html') 

def employe_detail_view(request,id):
    return render(request,'education/employe_detail.html') 

def parents_detail_view(request,id):
    return render(request,'education/parents_detail.html')     
    
def teacher_add_view(request):
    return render(request,'education/teacheradd.html')     

def groupslist_view(request):
    return render(request,'education/guruhlar.html')  

def roomslist_view(request):
    return render(request,'education/roomslist.html')

@login_required
def task_view(request):
    context = dict()
    context['tasks'] = Tasks.objects.all().order_by('-created_at')
    context['tasks'] = set_tasks_status(tasks=context['tasks'])
    context['whom'] = UserTaskStatus.objects.all()
    context['task_types'] = TaskTypes.objects.all()
    context['responsibles'] = CustomUser.objects.filter(Q(is_superuser=True)|Q(is_staff=True)).values('id', 'first_name', 'last_name')
    return render(request,'education/task.html', context=context)    

@login_required
def task_create_view(request):
    status=200
    form = TaskForm(request.POST or None, request.FILES)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.author = request.user
        task.status = 1
        task.save()
        form.save_m2m()
        status = 201
    else:
        return JsonResponse(form.errors, safe=False, status=400)
    return JsonResponse({'message':'ok'}, status=status)

def employees_view(request):
    return render(request,'education/employees.html') 

def students_list_view(request):
    return render(request,'education/students_list.html') 

def parents_list_view(request):
    context = {}
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter = EduCenters.objects.filter(qury)
    if request.method == "POST":
        post = request.POST
    educenter_ids = educenter.values_list('id',flat=True)    
    context['groups']  = list(GroupModel.groups.group_list(educenter_ids))
    context['courses'] = list(Course.courses.courses(educenter_ids,True))
    context['keys'] = ['check','title','course','teacher','days','times','total_student','course__price','action']
    return render(request,'education/parents_list.html',context)

def finance_list_view(request):
    return render(request,'education/finance_list.html')    

def expenses_list_view(request):
    return render(request,'education/expenses.html')

def debt_list_view(request):
    return render(request,'education/debt_list.html') 

def debt_groups_view(request,id):
    return render(request,'education/debt_groups.html')

def debt_course_view(request,id):
    return render(request,'education/debt_course.html')

def message_settings_view(request):
    return render(request,'education/message_settings.html') 

def lid_first_view(request):
    return render(request,'education/lid_first.html') 

def lid_sk_view(request):
    return render(request,'education/lid_sk.html') 

def lid_ry_view(request):
    return render(request,'education/lid_ry.html') 

def faqs(request, *args, **kwargs):
    content = get_object_or_404(Contents, pk=int(request.GET.get('content')))
    if request.method == 'POST':
        formset = FAQFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                faq = form.save(commit=False)
                faq.content = content
                if faq.content:
                    faq.save()
            return JsonResponse({'status': 201})
        else:
            print(formset.non_form_errors())
            return JsonResponse({"status": 400})
    faqs = FAQ.objects.filter(content=content)
    data = list()
    for faq in faqs:
        dct = model_to_dict(faq, fields=('id', 'question', 'answer'))
        data.append(dct)
    return JsonResponse({'faqs': data})


def faq_detail(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        faq.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'status': 'not deleted'})

def faq_update(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            faq = form.save()
            return JsonResponse(model_to_dict(faq, fields=('id', 'question', 'answer')), safe=False)
        return JsonResponse(form.non_field_errors(), status=400)
    return JsonResponse(model_to_dict(faq, fields=('id', 'question', 'answer')), safe=False)


def set_content_order(request, pk: int, order: int):
    content = get_object_or_404(Contents, pk=pk)
    content.order = order
    content.save()
    return JsonResponse({'status': 200})

@login_required
def online_course_contents_view(request, id):
    lesson = get_object_or_404(Lessons, pk=id)
    group = request.GET.get('group', None)
    if request.user.is_superuser:
        contents = lesson.contents.all()
        if group:
            contents = contents.filter(groups__in=[group]).values('id', 'title', 'content_type', 'status')
        else:
            contents = contents.values('id', 'title', 'content_type', 'status')
    else:
        admins = CustomUser.objects.filter(is_superuser=True)
        contents = lesson.contents.filter(Q(author=request.user)|Q(author__in=admins), groups__id=group).values('id', 'title', 'content_type', 'status')
    CONTENT_TYPES = {
        1: "Video", 2: "File", 3:"Test", 4:"Vazifa"
    }
    for content in contents:
        content['content_type'] = CONTENT_TYPES[content['content_type']]

    return JsonResponse(list(contents), safe=False)

def online_content_resources_view(request):
    if request.method == 'POST':
        resources = request.FILES.getlist('resources')
        pk = request.GET.get('content')
        content = get_object_or_404(Contents, pk=int(pk))
        for resource in resources:
            res, created = Resources.objects.get_or_create(content=content, file=resource)
            res.save()

        return JsonResponse({'status': 201})
    return JsonResponse({'status': 200})


@login_required
def modules_detail_view(request, pk):
    module = get_object_or_404(Modules, pk=pk)
    # if request.user in get_admins():
    #     lessons = module.lessons.all().values('id', 'title', 'order')
    # else:
    #     admins = CustomUser.objects.filter(is_superuser=True)
    #     lessons = module.lessons.filter(Q(author=request.user)|Q(author__in=admins)).values('id', 'title', 'order')
    # data['lessons'] = list(lessons)
    data = model_to_dict(module, fields=('id', 'title'))
    data['status'] = bool(Contents.objects.filter(lesson__module=module, status=True).count())
    return JsonResponse(data, safe=False)

@login_required
def online_content_resource_delete_view(request, pk):
    resource = get_object_or_404(Resources, pk=int(pk))
    message = "Siz GET so'rov yubordingiz."
    if request.method == 'POST':
        resource.delete()
        message = "O'chirildi."
    return JsonResponse({'method':request.method, 'message':message})

@login_required
def homeworks_view(request):
    context = dict()
    courses = get_courses(user=request.user)
    context['courses'] = get_courses_via_hws(courses, user=request.user)
    context['groups'] = get_groups_via_hws(courses, request.user)
    return render(request, 'education/uyga_vazifa_teacher.html', context)

def group_homeworks_detail_view(request, pk):
    context = dict()
    group = get_object_or_404(Group, pk=pk)
    context['group'] = model_to_dict(group, fields=('id', 'title'))
    context['group']['course'] = model_to_dict(group.course, fields=('id', 'title'))
    context['students'] = get_students_data(group=group)
    context['leads'] = get_leads_data(group=group)
    context['general'] = list(context['students'])+context['leads'] 
    return render(request, 'education/uyga_vazifa_ichki_teacher.html', context)


def student_homeworks_in_group(request, pk):
    group_student = get_object_or_404(GroupStudents, pk=pk)
    student = group_student.student
    course = group_student.group.course

    contents = get_contents(course, content_type=4)

    data = []
    for content in list(contents):
        dct = model_to_dict(content, fields=('id', 'title', 'text'))
        if content.homework:
            dct['homework'] = {'name':content.homework.name, 'url': content.homework.url}
        homeworks = content.homeworks.filter(student=student).order_by('date_created')
        dct['homeworks'] = []
        for homework in homeworks:
            hw = model_to_dict(homework, fields=('id', 'text', 'ball', 'date_created', 'date_modified', 'comment', 'status', ))
            hw['date_created'] = homework.date_created.strftime('%d/%m/%Y - %H:%M') if homework.date_created else ''
            hw['date_modified'] = homework.date_modified.strftime('%d/%m/%Y - %H:%M') if homework.date_modified else ''

            if homework.file:
                hw['homework'] = {'name':homework.file.name.split('/')[-1], 'url':homework.file.url}
            
            if homework.comment_file:
                hw['comment_file'] = {'name':homework.comment_file.name.split('/')[-1], 'url':homework.comment_file.url}
            hw['commented'] = homework.commented.full_name() if homework.commented else ''
            if Teacher.objects.filter(user=homework.commented).exists():
                hw['commenter'] = 'O\'qituvchi'
            else:
                hw['commenter'] = 'Admin' if homework.commented and homework.commented.is_superuser else 'Mas\'ul'
            dct['homeworks'].append(hw)
        if homeworks.last():
            dct['status'] = homeworks.last().status
        else:
            dct['status'] = 1   
        data.append(dct)
    return JsonResponse(data, safe=False)


def check_permission(request, homework):
    if request.user.is_superuser is False:
        teacher = request.user.teacher_set.first()
        groups = [group.group for group in homework.student.ggroups.all()]
        for group in groups:
            if group.teacher == teacher or group.trainer == teacher:
                return True
        return False
    return True
@login_required
def homework_edit_view(request, action, pk):
    ACTIONS = {
        'give-ball':3,
        'reject': 4
    }
    homework = get_object_or_404(Homeworks, pk=pk)
    
    permitted = check_permission(request, homework)
    if permitted is False:
        return JsonResponse({'status':'permitted'}, status=403)

    if request.method == 'POST':
        form = HomeworkActionForm(request.POST, request.FILES, instance=homework)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.status = ACTIONS[action]
            homework.commented = request.user
            homework.date_modified = timezone.now()
            homework.save()
            return JsonResponse({'status':"ok"}, status=200)
        else:
            print(form.errors())
            return JsonResponse({'status':'ok'}, safe=False)
    return JsonResponse({}, status=200)


def lead_homeworks_in_group(request, pk):
    demo = get_object_or_404(LeadDemo, pk=pk)
    lead = demo.lead
    group = demo.group
    contents = get_lead_homework_contents(lead=lead, group=group, content_type=4)
    data = []
    for content in list(contents):
        dct = model_to_dict(content, fields=('id', 'title', 'text'))
        if content.homework:
            dct['homework'] = {'name':content.homework.name, 'url': content.homework.url}
        homeworks = content.homeworks.filter(lead=lead).order_by('date_created')
        dct['homeworks'] = []
        for homework in homeworks:
            hw = model_to_dict(homework, fields=('id', 'text', 'ball', 'date_created', 'date_modified', 'comment', 'status', ))
            hw['date_created'] = homework.date_created.strftime('%d/%m/%Y - %H:%M') if homework.date_created else ''
            hw['date_modified'] = homework.date_modified.strftime('%d/%m/%Y - %H:%M') if homework.date_modified else ''

            if homework.file:
                hw['homework'] = {'name':homework.file.name.split('/')[-1], 'url':homework.file.url}
            
            if homework.comment_file:
                hw['comment_file'] = {'name':homework.comment_file.name.split('/')[-1], 'url':homework.comment_file.url}
            hw['commented'] = homework.commented.full_name() if homework.commented else ''
            if Teacher.objects.filter(user=homework.commented).exists():
                hw['commenter'] = 'O\'qituvchi'
            else:
                hw['commenter'] = 'Admin' if homework.commented and homework.commented.is_superuser else 'Mas\'ul'
            dct['homeworks'].append(hw)
        if homeworks.last():
            dct['status'] = homeworks.last().status
        else:
            dct['status'] = 1   
        data.append(dct)
    return JsonResponse(data, safe=False)