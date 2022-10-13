from modulefinder import Module
from django.db.models import Q, Count, F, Sum, QuerySet
from django.forms.models import model_to_dict
from django.utils import timezone 
from user.models import CustomUser
from education.models import Contents, Lessons, Modules
from admintion.models import Course, Student, Teacher, Group

from typing import List
def get_viewed_status(student, lesson_obj):
    if lesson_obj.contents.count() == 0:
        return False
    for content in lesson_obj.contents.all():
        if student not in content.students.all():
            return False
    return True

def get_opening_status(lesson_obj):
    if lesson_obj.contents.count() == 0:
        return False
    for content in lesson_obj.contents.all():
        if content.opened_at and content.opened_at > timezone.now():
            return False
    return True

def get_lesson_contents_data(lesson_obj: Lessons=None, lesson_id:int=None, student:Student=None, user:CustomUser=None):
    if lesson_obj:
        contents = lesson_obj.contents.all()
    elif lesson_id:
        contents = Contents.objects.filter(lesson_id=lesson_id)
    
    data = list()
    if student:
        for content in contents:
            data.append({
                'id': content.id,
                'title': content.title,
                'content_type': content.content_type,
                'viewed': bool(student in content.students.all()),
                'open': bool(content.opened_at and content.opened_at < timezone.now())
            })
    elif user:
        teacher = Teacher.objects.filter(user=user)
        if teacher:
            admins = CustomUser.objects.filter(is_superuser=True)
            contents = contents.filter(Q(author=user)|Q(author__in=admins))
        for content in contents:
            data.append({
                'id': content.id,
                'title': content.title,
                'content_type': content.content_type,
                'author': content.author
            })

    return data

def get_updated_modules(modules, user:CustomUser, with_lesson_contents=False):
    student = Student.objects.filter(user=user).first()

    for module in modules:
        lessons = list()
        for lesson in module['lessons']:
            lesson_obj = Lessons.objects.filter(id=lesson).first()
            if lesson_obj:
                if with_lesson_contents:
                    lessons.append({
                        'id': lesson, 
                        'title': lesson_obj.title, 
                        'viewed': get_viewed_status(student, lesson_obj),
                        'open': get_opening_status(lesson_obj),
                        'contents': get_lesson_contents_data(lesson_obj, student)
                    })
                else:
                    lessons.append({
                        'id': lesson, 
                        'title': lesson_obj.title, 
                        'viewed': get_viewed_status(student, lesson_obj),
                        'open': get_opening_status(lesson_obj)
                    })
        if len(lessons):
            module['lessons'] = lessons
        else:
            module['lessons'] = None
        
        if all([lesson['viewed'] for lesson in lessons]) and len(lessons) > 0:
            module['status'] = "Tugallangan"
            module['status_class'] = "success"
        elif any([lesson['viewed'] for lesson in lessons]) and len(lessons) > 0:
            module['status'] = "Jarayonda"
            module['status_class'] = "primary"
        else:
            module['status'] = ""
            module['status_class'] = ""
    return modules


def get_next_module(course:Course, last_order=None):
    if last_order:
        module = course.modules.filter(order__gt=last_order).first()
    else:
        module = course.modules.first()
    return module

def get_next_lesson(module:Modules, last_order=None):
    if last_order:
        lesson = module.lessons.filter(order__gt=last_order).first()
    else:
        lesson = module.lessons.first()
    if lesson:
        return lesson
    else:
        module = get_next_module(module.course, module.order)
        return get_next_lesson(module) if module else None

def get_need_content(lesson: Lessons, last_order=None):
    if last_order:
        content = lesson.contents.filter(order__gt=last_order).first()
    else:
        content = lesson.contents.first()
    
    if content:
        return content
    else:
        lesson = get_next_lesson(lesson.module, lesson.order)
        return get_need_content(lesson) if lesson else None

def get_courses_data(courses, teacher: Teacher=None):
    if type(courses) not in [list, QuerySet]:
        return []
    data = list()
    admins: List[CustomUser] = CustomUser.objects.filter(is_superuser=True)
    for course in set(courses):
        dct = model_to_dict(course, fields=('id', 'title'))
        if teacher:
            dct['group_count'] = course.group_set.filter(Q(teacher=teacher)|Q(trainer=teacher)).count()
        else:
            dct['group_count'] = course.group_set.count()
        lessons = Lessons.objects.filter(module__course=course)
        contents = Contents.objects.filter(lesson__in=lessons)
        if teacher:
            contents = contents.filter(Q(author=teacher.user)|Q(author__in=admins))
        dct['video_contents'] = contents.filter(content_type=1).count()
        dct['text_contents'] = contents.filter(content_type=2).count()
        dct['test_contents'] = contents.filter(content_type=3).count()
        dct['homework_contents'] = contents.filter(content_type=4).count()
        dct['contents'] = contents.count()

        data.append(dct)
    return data

def get_courses(user: CustomUser):
    teacher = Teacher.objects.filter(user=user).first()
    courses = list()
    if teacher and teacher.group_teacher.count() > 0:
        courses = [ group.course for group in teacher.group_teacher.all()]
    elif teacher and teacher.trainer.count() > 0:
        courses = [ group.course for group in teacher.trainer.all()]
    
    # Admin roli qanday?
    else:
        courses = Course.objects.all()
    print(courses)
    return get_courses_data(courses, teacher=teacher)

def get_groups_data(groups, teacher: Teacher=None):
    if type(groups) not in [List, QuerySet]:
        return []
    data = list()
    admins: List[CustomUser] = CustomUser.objects.filter(is_superuser=True)
    for group in set(groups):
        dct = model_to_dict(group, fields=('id', 'title', 'teacher'))
        dct['teacher'] = f"{group.teacher.user.full_name()}"
        dct['trainer'] = f"{group.trainer.user.full_name()}"
        dct['course'] = group.course.title
        lessons = Lessons.objects.filter(module__course=group.course)
        contents = Contents.objects.filter(Q(author__in=admins)|Q(author=group.teacher.user), lesson__in=lessons)
        if teacher:
            contents = contents.filter(Q(author=teacher.user)|Q(author__in=admins))
        dct['video_contents'] = contents.filter(content_type=1).count()
        dct['text_contents'] = contents.filter(content_type=2).count()
        dct['test_contents'] = contents.filter(content_type=3).count()
        dct['homework_contents'] = contents.filter(content_type=4).count()
        dct['contents'] = contents.count()

        data.append(dct)
    return data

def get_groups(user: CustomUser):
    teacher = Teacher.objects.filter(user=user).first()
    groups = list()
    if teacher and teacher.group_teacher.count() > 0:
        groups = Group.objects.filter(Q(teacher=teacher)|Q(trainer=teacher))

    # Admin roli qanday?
    else:
        groups = Group.objects.all()
    
    return get_groups_data(groups, teacher=teacher)


def get_modules_data(modules):
    data = list()
    for module in list(modules):
        dct = dict()
        dct = model_to_dict(module, fields=('id', 'title', 'author'))
        try:
            dct['author_name'] = module.author.full_name()
        except:
            dct['author_name'] = ''
        dct['lessons'] = list(module.lessons.all().values('id', 'title', 'order','author'))
        data.append(dct)
    return data

def get_modules(course:Course, user:CustomUser):
    teacher = Teacher.objects.filter(user=user).first()
    if teacher:
        admins = CustomUser.objects.filter(is_superuser=True)
        modules = course.modules.filter(Q(author=user)|Q(author__in=admins))
    else:
        modules = course.modules.all()
    return modules

def get_lessons_data(lessons):
    data = list()
    for lesson in lessons:
        dct = dict()
        dct = model_to_dict(lesson, fields=('id', 'title', 'author', 'order', 'module'))
        try:
            dct['author_name'] = lesson.author.full_name()
        except:
            dct['author_name'] = ''

        data.append(dct)

    return data

def get_lessons(course:Course, user:CustomUser, **filter_kwargs):
    teacher = Teacher.objects.filter(user=user).first()
    print(filter_kwargs)
    if teacher:
        admins = CustomUser.objects.filter(is_superuser=True)
        lessons = Lessons.objects.filter(Q(author=user)|Q(author__in=admins), module__course=course, **filter_kwargs)
    else:
        lessons = Lessons.objects.filter(module__course=course, **filter_kwargs)
    return lessons