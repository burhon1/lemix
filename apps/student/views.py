from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.urls import reverse
from admintion.models import GroupStudents, Student, Payment, Course
from education.models import Modules, Lessons, Contents, Tests
from student.models import Homeworks, TestResults, StudentAnswers
from education.selectors import get_updated_modules, get_need_content
from education.services import set_student_viewed_content
from student.selectors import (
    get_student_courses, get_student_homeworks, get_student_tests, get_test_data,
    get_questions_for_student,
)

@login_required
def student_view(request):
    student = get_object_or_404(Student, user=request.user)
    context = {
        'student': model_to_dict(student)
    }
    if request.method == 'POST':
        # set student payments
        pass
    context.setdefault('balance', student.balance )
    payments = Payment.payments.student_payments(student.id)
    context.setdefault('payments', payments)
    group_student_objs = GroupStudents.custom_manager.student_groups(student.id)
    context.setdefault('groups', group_student_objs)
    return render(request, 'student/student.html', context)


def student_detail_view(request, pk):
    return render(request, 'student/student_detail.html', {})

@login_required
def my_courses_view(request):
    student = get_object_or_404(Student, user=request.user)
    group_student_objs = GroupStudents.custom_manager.student_groups(student.id)
    context = {'groups': group_student_objs}
    print(context)
    return render(request, 'student/kurslar_royxati.html', context)

@login_required
def course_modules_view(request, id):
    course = Course.courses.course(id=id)
    context = {'course': course}
    context['modules'] = Modules.modules.course_modules(id)
    context['modules'] = get_updated_modules(context['modules'], request.user)
    return render(request, 'student/content_royxati.html', context)


def rating_view(request):
    return render(request, 'student/reyting.html', {})

@login_required
def exams_view(request):
    student = get_object_or_404(Student, user=request.user)
    context = dict()
    context['exams'] = get_student_tests(student)
    return render(request, 'student/imtihonlar_royxati.html', context)

@login_required
def exam_view(request, pk: int):
    context = dict()
    student = get_object_or_404(Student, user=request.user)
    test = get_object_or_404(Tests, pk=pk)
    context['test'] = get_test_data(test)
    context['questions'] = get_questions_for_student(test, student) # bu StudentAnswers classi obyektlari
    print(context)
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
    context['modules'] = get_updated_modules(context['modules'], request.user, with_lesson_contents=True)
    context['resources'] = lesson.resources.all()
    context['faqs'] = content.faqs.all().values('question', 'answer')
    print("\n\n", context['content'], "\n\n")
    print("\n\n", context['modules'], "\n\n")
    print("\n\n", context['resources'], "\n\n")
    
    student = Student.objects.filter(user=request.user).first()
    if student and student not in content.students.all():
        set_student_viewed_content(student, content)
    return render(request, template_name, context)


def homework_detail_view(request, id):
    return render(request, 'student/uyga_vazifa_ichki.html', {})

def homeworks_view(request):
    student = get_object_or_404(Student, user=request.user)
    context = dict()
    context['homeworks'] = get_student_homeworks(student)
    return render(request, 'student/uyga_vazifa.html', context)

def help_view(request):
    return render(request, 'student/yordam.html')

@login_required
def student_homework_view(request, pk: int):
    student = get_object_or_404(Student, user=request.user)
    content = get_object_or_404(Contents, pk=pk)
    status = 400

    if request.method == 'POST':
        text = request.POST.get('text', None)
        file = request.FILES.get('file', None)

        if text is None and file is None:
            pass
        else:
            homework = Homeworks.objects.create(
                student=student, 
                content=content, 
                text=text, 
                file=file
                )
            status = 200

    return JsonResponse({'status': status})
    