from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.urls import reverse
from admintion.models import GroupStudents, Student, Payment, Course, FormLead, LeadDemo, Group
from education.models import Modules, Lessons, Contents, Tests
from education.selectors import get_updated_modules, get_need_content
from education.services import set_student_viewed_content
from student.selectors import (
    get_student_courses, get_student_homeworks, get_student_tests, get_test_data,get_lead_homeworks,
    get_questions_for_student,get_lead_updated_modules,check_lead_to_content_view_permision
)
from student.services import set_lead_content_viewed_status
from student.forms import HomeworkForm
from user.models import CustomUser
from user.utils import get_admins

@login_required
def student_view(request):
    student = get_object_or_404(Student, user=request.user)
    context = {
        'student': model_to_dict(student)
    }
    context.setdefault('balance', student.balance )
    payments = Payment.payments.student_payments(student.id)
    context.setdefault('payments', payments)
    group_student_objs = GroupStudents.custom_manager.student_groups(student.id)
    context.setdefault('groups', group_student_objs)
    context = {}
    context['is_student'] = True
    return render(request, 'student/student.html',context)


def student_detail_view(request, pk):
    return render(request, 'student/student_detail.html', {})

# @login_required
def my_courses_view(request):
    student = get_object_or_404(Student, user=request.user)
    group_student_objs = GroupStudents.custom_manager.student_groups(student.id)
    context = {'groups': group_student_objs}
    context['is_student'] = True
    return render(request, 'student/kurslar_royxati.html')

@login_required
def course_modules_view(request, id):
    course = Course.courses.course(id=id)
    context = {'course': course}
    context['modules'] = Modules.modules.course_modules(id)
    context['modules'] = get_updated_modules(context['modules'], request.user)
    context['is_student'] = True
    return render(request, 'student/content_royxati.html', context)


def rating_view(request):
    return render(request, 'student/reyting.html', {})

@login_required
def exams_view(request):
    student = get_object_or_404(Student, user=request.user)
    context = dict()
    context['exams'] = get_student_tests(student)
    context['is_student'] = True
    return render(request, 'student/imtihonlar_royxati.html', context)

@login_required
def exam_view(request, pk: int):
    context = dict()
    student = get_object_or_404(Student, user=request.user)
    test = get_object_or_404(Tests, pk=pk)
    context['test'] = get_test_data(test)
    context['questions'] = get_questions_for_student(test, student) # bu StudentAnswers classi obyektlari
    context['is_student'] = True
    return render(request, 'student/test_ichki_sahifasi.html', context)

@login_required
def lesson_detail_view(request, type:str, pk):
    template_name = 'student/darsnig_ichki_sahifasi_video.html'
    if type == 'lesson':
        lesson = get_object_or_404(Lessons, pk=pk)
        content = get_need_content(lesson)
    elif type == 'content':
        content = get_object_or_404(Contents, pk=pk)
        lesson = content.lesson
    elif type == 'next-content':
        content = get_object_or_404(Contents, pk=pk)
        if content.lesson:
            content = get_need_content(content.lesson, last_order=content.order)
        lesson = content.lesson
    else:
        return render(request, template_name, {})
    context = dict()
    context.setdefault('lesson', lesson)
    if content:
        context['content'] = model_to_dict(content, exclude=['lesson', 'students'])
        context['content']['value'] = content.get_value
    context['modules'] = Modules.modules.course_modules(lesson.module.course_id)
    if request.GET.get('group', None):
        context['modules'] = context['modules'].filter(groups__in=[int(request.GET.get('group'))])
    context['modules'] = get_updated_modules(context['modules'], request.user, with_lesson_contents=True)
    context['resources'] = content.content_resources.all()
    context['faqs'] = content.faqs.all().values('question', 'answer')
    context['homeworks'] = content.homeworks.filter(student__user=request.user)
    if len(context['homeworks']) and context['homeworks'].last().status==3:
        context['balled'] = True
    context['lesson'] = content.lesson
    student = Student.objects.filter(user=request.user).first()
    if student and student not in content.students.all():
        set_student_viewed_content(student, content)
    context['is_student'] = True
    return render(request, template_name, context)


def homework_detail_view(request, id):
    return render(request, 'student/uyga_vazifa_ichki.html', {})

def homeworks_view(request):
    student = get_object_or_404(Student, user=request.user)
    context = dict()
    context['homeworks'] = get_student_homeworks(student) 
    context['is_student'] = True
    return render(request, 'student/uyga_vazifa.html', context)

def help_view(request):
    return render(request, 'student/yordam.html')

@login_required
def student_homework_view(request, pk: int):
    student = get_object_or_404(Student, user=request.user)
    content = get_object_or_404(Contents, pk=pk)
    status = 400

    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.student=student 
            homework.content=content
            homework.status = 2
            homework.save()
            status = 201
        else:
            return JsonResponse(form.errors, safe=False, status=400)
    return JsonResponse({'status': status})
    

@login_required
def lead_view(request):
    lead = get_object_or_404(FormLead, user=request.user)
    context = {'lead': lead}
    return render(request, 'student/student.html', context)


@login_required
def lead_demos_view(request):
    lead = get_object_or_404(FormLead, user=request.user, activity=1)
    context = {'demos': LeadDemo.objects.filter(lead=lead)}
    groups = set([demo.group for demo in context['demos']])
    context['demos2'] = []
    for group in groups:
        context['demos2'].append(context['demos'].filter(group=group).first())
    context['demos'],context['demos2'] = context['demos2'], None
    return render(request, 'student/kurslar_royxati.html', context)

@login_required
def lead_course_modules_view(request, pk):
    course = Course.courses.course(id=pk)
    context = {'course': course}
    group = request.GET.get('group', False)
    authors = list(get_admins())
    if group:
        demo = request.user.lead.demo.filter(group_id=group).first()    
    else:
        demo = request.user.lead.demo.filter(group__course_id=course['id']).first()
    if demo and demo.group and demo.group.teacher:
        authors.append(demo.group.teacher.id)
    if demo and demo.group and demo.group.trainer:
        authors.append(demo.group.trainer.id)

    context['modules'] = Modules.modules.course_modules(pk).filter(author_id__in=authors)
    context['modules'] = get_lead_updated_modules(course['id'], context['modules'], request.user,authors=authors)
    context['group'] = group
    return render(request, 'student/lead_content_royxati.html', context)

@login_required
def lead_course_content_view(request, pk, lesson_id, module_id, course_id):
    lead = get_object_or_404(FormLead, user=request.user, activity=1)
    group = request.GET.get('group', False)
    authors = list(get_admins())
    if group:
        group = Group.objects.filter(id=group).first()
    else:
        demo = LeadDemo.objects.filter(lead=lead, group__in=Group.objects.filter(course_id=course_id)).first()
        if demo:
            group = demo.group
    if group:
        authors.append(group.teacher.user)
        authors.append(group.trainer.user) if group.trainer else authors

    content = get_object_or_404(Contents, pk=pk, author__in=authors, status=True)
    if check_lead_to_content_view_permision(lead, content) is False:
        return redirect('student:lead-demos')
    content = set_lead_content_viewed_status(content, lead)
    context = {'content': content, }
    context['modules'] = Modules.modules.course_modules(course_id)
    context['modules'] = get_lead_updated_modules(course_id, context['modules'], request.user, authors=authors, with_contents=True)
    context['lesson'] = content.lesson
    context['resources'] = content.content_resources.all()
    context['faqs'] = content.faqs.all()
    context['homeworks'] = content.homeworks.filter(lead__user=request.user)
    if len(context['homeworks']) and context['homeworks'].last().status==3:
        context['balled'] = True
    next = Contents.objects.filter(lesson_id=lesson_id, order__gt=content.order, status=True, author__in=authors).first()
    if next is None:
        lesson = Lessons.objects.filter(module_id=module_id, id=lesson_id, author__in=authors).first()
        lesson = Lessons.objects.filter(module_id=module_id, author__in=authors, order__gt=lesson.order).first()
        if lesson:
            next =lesson.contents.filter(author__in=authors, status=True).order_by('order').first()
        else:
            module = Modules.objects.filter(id=module_id, author__in=authors).first()
            module = Modules.objects.filter(order__gt=module.order, author__in=authors).first()
            if module:
                lessons = module.lessons.filter(author__in=authors)
                next = Contents.objects.filter(lesson__in=lessons, status=True).order_by('lesson__module', 'lesson', 'order').first()

    if next and check_lead_to_content_view_permision(lead, next):
        context['course_id'] = next.lesson.module.course_id
        context['module_id'] = next.lesson.module.id
        context['lesson_id'] = next.lesson.id
        context['next'] = next.id
    elif next is None:
        context['last'] = True
    context['group'] = group.id if group else ''
    return render(request, 'student/lead_darsnig_ichki_sahifasi_video.html', context)

@login_required
def lead_homeworks_view(request):
    lead = get_object_or_404(FormLead, user=request.user)
    context = {
        'homeworks': get_lead_homeworks(lead)
    }
    return render(request, "student/lead_uyga_vazifa.html", context)

@login_required
def lead_homework_view(request, pk: int):
    student = get_object_or_404(FormLead, user=request.user)
    content = get_object_or_404(Contents, pk=pk)
    status = 400

    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.lead=student 
            homework.content=content
            homework.status = 2
            homework.save()
            status = 201
        else:
            return JsonResponse(form.errors, safe=False, status=400)
    return JsonResponse({'status': status})