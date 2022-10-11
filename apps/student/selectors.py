from django.db.models import Q
from django.utils import timezone
from typing import List
from admintion.models import Student, GroupStudents
from education.models import Modules, Lessons, Contents, Questions, Tests
from student.models import Homeworks, TestResults, StudentAnswers

import random

def get_student_courses(student_id: int):
    group_students = GroupStudents.objects.filter(student_id=student_id)
    groups = [group.group for group in group_students ]
    courses = [group.course.id for group in groups ]
    return courses

def get_homeworks(courses: List[int]):
    modules = Modules.objects.filter(course_id__in=courses).values('id')
    lessons = Lessons.objects.filter(module_id__in=modules).values('id')
    homeworks = Contents.objects.filter(lesson_id__in=lessons, content_type=4).order_by('lesson__module__order').values('id', 'title', 'opened_at', 'closed_at', 'order')
    
    return homeworks

def get_student_homeworks(student: Student):
    courses = get_student_courses(student)
    homeworks = list(get_homeworks(courses))
    
    for content in homeworks:
        homework = Homeworks.objects.filter(student=student, content_id=content['id']).last()
        if homework:
            content.setdefault('homework', homework.id)
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