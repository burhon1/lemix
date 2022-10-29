from django.db.models import Q
from django.utils import timezone
from django.forms.models import model_to_dict
from typing import List
from admintion.models import Group, LeadDemo, Student, GroupStudents, FormLead, Course
from education.models import Modules, Lessons, Contents, Questions, Tests
from student.models import Homeworks, TestResults, StudentAnswers
from user.models import CustomUser

import random

def get_student_courses(student_id: int):
    group_students = GroupStudents.objects.filter(student_id=student_id)
    groups = [group.group for group in group_students ]
    courses = [group.course.id for group in groups ]
    return courses

def get_homeworks(courses: List[int], authors: List[CustomUser]):
    modules = Modules.objects.filter(course_id__in=courses).values('id')
    lessons = Lessons.objects.filter(module_id__in=modules).values('id')
    homeworks = Contents.objects.filter(lesson_id__in=lessons, content_type=4, status=True, author__in=authors).order_by('lesson__module__order').values('id', 'title', 'opened_at', 'closed_at', 'order')
    
    return homeworks

def get_content_authors_for_student(student: Student):
    groups = [ggroup.group for ggroup in student.ggroups.all()]
    teachers = [group.teacher.user for group in groups if group.teacher]
    trainers = [group.trainer.user for group in groups if group.trainer]
    admins = CustomUser.objects.filter(is_superuser=True)

    return list(admins)+teachers+trainers

def get_student_homeworks(student: Student):
    authors = get_content_authors_for_student(student)
    courses = get_student_courses(student)
    homeworks = list(get_homeworks(courses, authors=authors))
    
    for content in homeworks:
        homework = Homeworks.objects.filter(student=student, content_id=content['id']).last()
        if homework:
            content.setdefault('homework', model_to_dict(homework, fields=('id', 'ball', 'status', 'date_created', 'date_modified')))
            
            content.setdefault('ball', homework.ball)
        if content['opened_at']:
            content['times']: content['opened_at'].strftime("%d.%m.%Y")+ content['opened_at'].strftime("%H:%M - ") + content['closed_at'].strftime("%H:%M")
        if content['closed_at'] and content['closed_at'] < timezone.now():
            content['closed'] = True
        else:
            content['closed'] = False
    return homeworks

def get_tests(courses: List[int]):
    modules = Modules.objects.filter(course_id__in=courses)
    lessons = Lessons.objects.filter(module__in=modules)
    tests = Tests.objects.filter(
        Q(course_id__in=courses)|Q(module__in=modules)|Q(lesson__in=lessons)
        )

    return tests

def get_student_tests(student: Student):
    courses = get_student_courses(student)
    tests = get_tests(courses)
    data = list()
    for test in tests:
        dct = dict()
        if test.course:
            dct['id'] = test.id
            dct['title'] = test.course.title + ' fani yuzasidan test'
        elif test.module:
            dct['title'] = test.module.title + ' moduli yuzasidan test'
        elif test.lesson:
            dct['title'] = test.lesson.title + ' mavzu yuzasidan test'
        dct['count_per_student'] = test.count_per_student
        dct['answer'] = TestResults.objects.filter(student=student, test=test).last()
        if test.opened_at and test.closed_at:
            dct['time'] = f"%s %s - %s" %(
                test.opened_at.strftime('%d.%m.%Y, '), test.opened_at.strftime('%H:%M'), test.closed_at.strftime('%H:%M'), 
            )
            dct['closed'] = not test.opened_at < timezone.now() < test.closed_at
        if test.questions.count() > test.count_per_student:
            dct['available'] = True
        else:
            dct['available'] = False # Test savollari soni yetarli emas.
        data.append(dct)
    print(data)
    return data

def get_test_data(test):
    dct = dict()
    if test.course:
        dct['title'] = test.course.title + ' fani yuzasidan test'
    elif test.module:
        dct['title'] = test.module.title + ' moduli yuzasidan test'
    elif test.lesson:
        dct['title'] = test.lesson.title + ' mavzu yuzasidan test'
    dct['count_per_student'] = test.count_per_student
    if test.opened_at and test.closed_at:
        dct['time'] = f"%s %s - %s" %(
            test.opened_at.strftime('%d.%m.%Y, '), test.opened_at.strftime('%H:%M'), test.closed_at.strftime('%H:%M'), 
        )
        dct['closed'] = not test.opened_at < timezone.now() < test.closed_at

    return dct

def get_questions_data(questions: List[StudentAnswers]):
    """
    Test savollarini dict ko'rinishida qaytaradi.
    questions -> StudentAnswers modelining obyektlari.
    """
    data = list()
    for question in questions:
        dct = dict()
        dct['id'] = question.id
        dct['question'] = {
            'id':question.question.id, 
            'question':question.question.question, 
            'answers':question.question.answers.all().values('id', 'answer')
            }
        dct['answer'] = question.answer.id if question.answer else None
        data.append(dct)
    return data


def get_questions_for_student(test:Tests, student:Student):
    """ 
    testni tekshiradi, savollar sonini tekshiradi, o'quvchiga test va test savollari biriktirib qaytaradi.
    """
    test_result_obj = TestResults.objects.create(test=test, student=student)
    questions = StudentAnswers.objects.filter(student=student, test_result=test_result_obj).last()
    if questions:
        return get_questions_data(questions)
    test_questions = Questions.objects.filter(test=test)
    counter = test.count_per_student
    
    if counter > test_questions.count():
        return []
    questions = list()
    used_questions = list()
    while counter: 
        question = random.choice(list(test_questions))
        if question not in used_questions:
            student_question = StudentAnswers.objects.create(student=student, test_result=test_result_obj, question=question)
            questions.append(student_question)
            used_questions.append(question)
            counter -= 1
    return get_questions_data(questions)

def get_lead_viewing_content(contents, lead, is_open_one=True):
    print(is_open_one)
    data = []
    for content in contents:
        dct = model_to_dict(content, fields=('id', 'title', 'content_type'))
        dct['viewed'] = bool(lead in content.leads.all())
        if dct['viewed'] is True:
            dct['open'] = True
        elif is_open_one:
            dct['open'], is_open_one = True, False
        else:
            dct['open'] = False
        data.append(dct)

    return data

def get_lead_updated_modules(course_id:int, modules:Modules, user:CustomUser, with_contents=False):
    lead = FormLead.objects.filter(user=user).first()
    groups = Group.objects.filter(course_id=course_id)
    demos = len(LeadDemo.objects.filter(lead=lead, group__in=groups))
    module_data = []
    
    for module in modules:
        initial = True
        module['lessons'] = []
        lesson_objs = Lessons.objects.filter(module_id=module['id']).order_by('order')
        for lesson in lesson_objs:
            dct = model_to_dict(lesson, fields=('id', 'title', 'order'))
            contents = lesson.contents.filter(status=True).order_by('order')
            dct['content'] = contents[0].id if len(contents)>0 else None
            dct['viewed'] = bool(contents.filter(leads__in=[lead]))
            if demos:
                dct['open'], demos = initial, demos-1
            else:
                dct['open'] = False
            if with_contents:
                dct['contents'] = get_lead_viewing_content(contents, lead, initial)
            if dct['content'] is not None:
                module['lessons'].append(dct)
            if dct['viewed'] is False:
                initial = False
        if module['lessons'] != []:
            module_data.append(module)

    return module_data


def check_lead_to_content_view_permision(lead:FormLead, content:Contents):
    course = content.lesson.module.course
    groups = Group.objects.filter(course=course)
    demos = len(LeadDemo.objects.filter(lead=lead, group__in=groups))
    modules = course.modules.all()
    lessons = Lessons.objects.filter(module__in=modules).order_by('module', 'order')[:demos]
    for lesson in lessons:
        if content in lesson.contents.filter(status=True):
            return True

    return False