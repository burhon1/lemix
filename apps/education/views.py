from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from admintion.models import Course
from education.models import FAQ, Lessons, Modules, Contents, Resources
from education.selectors import get_courses, get_groups, get_lesson_contents_data, get_modules, get_modules_data, get_lessons, get_lessons_data, get_courses_data
from education.forms import LessonAddForm, ContentForm, FAQFormSet, TextContentForm
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
    context['courses'] = get_courses(request.user)
    context['groups'] = get_groups(request.user)
    return render(request,'education/onlin.html', context) 

@login_required
def onlin_video_view(request, pk):
    content = get_object_or_404(Contents, pk=pk)
    context = dict()
    context['resources'] = content.content_resources.values('id', 'file', 'link')
    context['faqs'] = content.faqs.values('id', 'question', 'answer')
    context['content'] = model_to_dict(content, fields=('id', 'title', 'video', 'video_link', 'text', 'required'))
    context['action'] = 'tahrirlash'
    return render(request,'education/onlin_video.html', context=context) 

@login_required
def onlin_video_create_view(request, lesson_id):
    if request.method == 'POST':
        lesson = get_object_or_404(Lessons, id=lesson_id)
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            if content.video is None and content.video_link is None:
                return JsonResponse({'message': 'Video fayl yoki havola yuklashingiz kerak'}, status=400)
            content.content_type = 1 
            content.lesson = lesson 
            content.author = request.user
            content.save()
            return JsonResponse({'message':'created'}, status=201)
        else:
            return JsonResponse({'message':form.non_field_errors()}, status=400)
    # return JsonResponse({'message':'so\'rov metodi to\'g\'ri emas.'}, status=400)
    return render(request,'education/onlin_video.html')

@login_required
def onlin_text_view(request, lesson_id):
    lesson = get_object_or_404(Lessons, id=lesson_id)
    if request.method == 'POST':
        form = ContentForm(request.POST)
        
        if form.is_valid():
            content = form.save(commit=False)
            content.author = request.user 
            content.content_type = 2
            content.lesson = lesson
            content.save()
            print(model_to_dict(content, fields=('id', 'lesson', 'text', 'required', 'status')))
            return JsonResponse(model_to_dict(content, fields=('id', 'lesson', 'text', 'required', 'status')))
        else:
            print(form.non_field_errors())
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
        return JsonResponse(context['content'], status=200)

    return render(request,'education/onlin_text.html', context) 

def onlin_test_view(request):
    return render(request,'education/onlin_test.html') 

def onlin_hwork_view(request):
    return render(request,'education/onlin_hwork.html') 

@login_required
def onlins_view(request,id):
    course = get_object_or_404(Course, id=id)
    context = dict()
    context['course'] = get_courses_data([course], teacher=request.user.teacher_set.first())[0]
    
    if request.method == 'POST':
        lesson_id = request.POST.get('lesson')
        if lesson_id:
            context['contents'] = get_lesson_contents_data(lesson_id=lesson_id, user=request.user)
        module_id = request.POST.get('module')
        if module_id:
            filter_kwargs = {'module_id': module_id}
            context['lessons'] = get_lessons(course, request.user,**filter_kwargs)
            context['lessons'] = get_lessons_data(context['lessons'])
            print(context["lessons"])
        return JsonResponse(context)

    context['modules'] = get_modules(course, request.user)
    module_id = request.GET.get('m', None)
    filter_kwargs = dict()
    if module_id:
        filter_kwargs = {'module_id': module_id,}
    context['lessons'] = get_lessons(course, request.user, **filter_kwargs)
    context['lessons'] = get_lessons_data(context['lessons'])
    context['modules'] = get_modules_data(context['modules'])
    print("\n\n", context, "\n\n")
    return render(request,'education/onlins.html', context) 

@login_required
def online_delete_view(request, id):
    course = get_object_or_404(Course, id=id)
    if course.author == request.user or request.user.is_superuser:
        course.modules.all().delete()
        course.tests_set.all().delete()
        return redirect('education:onlins', kwargs={'id':id}) 
    return JsonResponse({'status':'Sizda bunga ruhsat yo\'q'})

@login_required
def modules_view(request):
    if request.user.is_superuser:
        pass
    elif request.user.teacher_set.first():
        pass
    else:
        JsonResponse({'status':403, 'message': 'Siz bunday operatsiyani bajara olmaysiz'})
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        course_id =  request.POST.get('course_id')
        course = Course.objects.filter(id=course_id).first()
        module:Modules = None
        try:
            module = Modules.objects.create(title=name, comment=description, course=course, author=request.user)
            message = 'Bo\'lim yaratildi'
        except:
            
            message = 'Bunday bo\'limni yaratib bo\'lmaydi'
    if module:
        module = model_to_dict(module)
    return JsonResponse({'message': message, 'module': module})


@login_required
def course_modules_view(request, pk):
    course = Course.objects.filter(id=pk).first()
    modules = get_modules(course, request.user)
    context = dict()
    context['modules'] = list(get_modules_data(modules))
    return JsonResponse(context)


@login_required
def create_lesson_view(request):
    if request.method == 'POST':
        data = request.POST
        form = LessonAddForm(data)
        if form.is_valid():
            lesson = form.save(author=request.user)
            return JsonResponse({'lesson': model_to_dict(lesson), 'status': 201} )
        print(form.errors)
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

def task_view(request):
    return render(request,'education/task.html')    

def employees_view(request):
    return render(request,'education/employees.html') 

def students_list_view(request):
    return render(request,'education/students_list.html') 

def parents_list_view(request):
    return render(request,'education/parents_list.html')

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

def set_content_order(request, pk: int, order: int):
    content = get_object_or_404(Contents, pk=pk)
    if content.order > order:
        query = Q()
    contents = Contents.objects.filter()
    
    content.order = order
    content.save()
    return JsonResponse({'status': 200})


def online_course_contents_view(request, id):
    lesson = get_object_or_404(Lessons, pk=id)

    contents = lesson.contents.values('id', 'title', 'content_type', 'status')
    CONTENT_TYPES = {
        1: "Video", 2: "File", 3:"Test", 4:"Vazifa"
    }
    for content in contents:
        content['content_type'] = CONTENT_TYPES[content['content_type']]

    return JsonResponse(list(contents), safe=False)

def online_content_resources_view(request):
    if request.method == 'POST':
        resources = request.FILES.getlist('resources')
        pk = request.POST.get('content')
        content = get_object_or_404(Contents, pk=pk)
        print(resources)
        for resource in resources:
            res, created = Resources.objects.get_or_create(content=content, file=resource)
            print(res.file)
        return JsonResponse({'status': 201})
    return JsonResponse({'status': 200})


@login_required
def modules_detail_view(request, pk):
    module = get_object_or_404(Modules, pk=pk)
    lessons = module.lessons.values('id', 'title', 'order')

    return JsonResponse(lessons, safe=False)