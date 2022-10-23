from django.db.models import Q, Count, F, Sum, QuerySet, Value
from django.db.models.functions import Concat
from django.forms.models import model_to_dict
from django.utils import timezone
from student.models import Homeworks 
from user.models import CustomUser
from education.models import Contents, Lessons, Modules
from admintion.models import Course, GroupStudents, Student, Teacher, Group

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

def get_lesson_contents_data(lesson_obj: Lessons=None, lesson_id:int=None, student:Student=None, user:CustomUser=None, authors=[], group:Group=None):
    query = dict()
    if len(authors):
        query['author__in'] = authors
    if lesson_obj:
        query['lesson_id'] = lesson_obj.id
    if lesson_id:
        query['lesson_id'] = lesson_id
    if group:
        query['groups__in'] = [group]
    contents = Contents.objects.filter(**query)
    
    data = list()
    if student:
        for content in contents:
            data.append({
                'id': content.id,
                'title': content.title,
                'content_type': content.content_type,
                'viewed': bool(student in content.students.all()),
                'open': bool(content.opened_at and content.opened_at < timezone.now() or content.status)
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
    authors = CustomUser.objects.filter(is_superuser=True)
    group = None
    if len(modules):
        module = Modules.objects.filter(id=modules[0]['id']).first()
        course = module.course if module else None 
        group = student.ggroups.filter(group__course=course).first().group
        authors = list(authors)
        authors.append(group.teacher.user)
        authors.append(group.trainer.user)

    for module in modules:
        lessons = list()
        lessons_qs = Lessons.objects.filter(module_id=module['id'], author__in=authors)
        if group:
            lessons_qs = lessons_qs.filter(groups__in=[group])
        for lesson in lessons_qs: 
            
            if with_lesson_contents:
                lessons.append({
                    'id': lesson.id, 
                    'title': lesson.title, 
                    'viewed': get_viewed_status(student, lesson),
                    'open': get_opening_status(lesson),
                    'contents': get_lesson_contents_data(lesson_obj=lesson, student=student, authors=authors, group=group)
                })
            else:
                lessons.append({
                    'id': lesson.id, 
                    'title': lesson.title, 
                    'viewed': get_viewed_status(student, lesson),
                    'open': get_opening_status(lesson)
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
    if course is None:
        return None
    if last_order:
        module = course.modules.filter(order__gt=last_order).first()
    else:
        module = course.modules.first()
    return module

def get_next_lesson(module:Modules, last_order=None):
    if module is None:
        return None
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
    if lesson is None:
        return None
    if last_order:
        content = lesson.contents.filter(order__gt=last_order).first()
    else:
        content = lesson.contents.first()
    
    if content:
        return content
    else:
        lesson = get_next_lesson(lesson.module, lesson.order)
        if lesson:
            return get_need_content(lesson)
        else:
            return None

def get_courses_data(courses, teacher: Teacher=None):
    if type(courses) not in [set, list, QuerySet]:
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
        dct['status'] = bool(contents.filter(status=True).count())
        data.append(dct)
    return data

def get_courses(user: CustomUser):
    teacher = Teacher.objects.filter(user=user).first()
    courses = list()
    if teacher and teacher.group_teacher.count() > 0:
        courses += [ group.course for group in teacher.group_teacher.all()]
    if teacher and teacher.trainer.count() > 0:
        courses += [ group.course for group in teacher.trainer.all()]
    
    # Admin roli qanday?
    else:
        courses = Course.objects.all()
    print(courses)
    return set(courses)

def get_groups_data(groups, teacher: Teacher=None):
    if type(groups) not in [set, list, QuerySet]:
        return []
    data = list()
    admins: List[CustomUser] = CustomUser.objects.filter(is_superuser=True)
    for group in set(groups):
        dct = model_to_dict(group, fields=('id', 'title', 'teacher'))
        dct['teacher'] = f"{group.teacher.user.full_name()}"
        dct['trainer'] = f"{group.trainer.user.full_name()}"
        dct['course'] = {
            'title': group.course.title, 'id': group.course.id
        }

        lessons = Lessons.objects.filter(groups__id=group.id) #module__course=group.course
        query = Q(author__in=admins)|Q(author=group.teacher.user)
        if group.trainer:
            query = query|Q(author=group.trainer.user)
        contents = Contents.objects.filter((query), lesson__in=lessons, groups__id=group.id)
        if teacher:
            contents = contents.filter(Q(author=teacher.user)|Q(author__in=admins))
        dct['video_contents'] = len(contents.filter(content_type=1))
        dct['text_contents'] = len(contents.filter(content_type=2))
        dct['test_contents'] = len(contents.filter(content_type=3))
        dct['homework_contents'] = len(contents.filter(content_type=4))
        dct['contents'] = len(contents)
        print(group, dct)
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


def get_modules_data(modules, group=None, authors=[]):
    data = list()
    for module in list(modules):
        dct = dict()
        dct = model_to_dict(module, fields=('id', 'title', 'author'))
        try:
            dct['author_name'] = module.author.full_name()
        except:
            dct['author_name'] = ''
        lessons = module.lessons.all()
        query = dict()
        if group:
            query.update({'groups__id': group.id })
        if authors and len(authors)>0:
            query.update({'author__in':authors})
            # dct['lessons'] = list(module.lessons.filter(groups__id=group.id).values('id', 'title', 'order','author'))
        dct['lessons'] = list(lessons.filter(**query).values('id', 'title', 'order','author'))
        dct['status'] =  bool(Contents.objects.filter(lesson__module=module, status=True).exists())
        data.append(dct)
    return data

def get_modules(course:Course, user:CustomUser, group:Group=None):
    teacher = Teacher.objects.filter(user=user).first()
    if teacher:
        admins = CustomUser.objects.filter(is_superuser=True)
        modules = course.modules.filter(Q(author=user)|Q(author__in=admins))
    else:
        modules = course.modules.all()
    if group:
        return modules.filter(groups__id=group.id)
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
        dct['status'] = bool(Contents.objects.filter(lesson=lesson, status=True).count())
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
    return lessons.order_by('module', 'order')


def get_courses_via_hws(courses, user:CustomUser):
    if type(courses) not in [set, list, QuerySet]:
        return []
    admins = CustomUser.objects.filter(is_superuser=True)
    data = list()
    for course in list(courses):
        dct = model_to_dict(course, fields=('id', 'title',))
        dct['groups'] = len(course.group_set.all())
        dct['students'] = len(GroupStudents.objects.filter(group__course=course))
        modules = course.modules.all()
        if user.teacher_set.exists():
            homeworks = Contents.objects.filter(Q(author=user)|Q(author__in=admins), lesson__module__in=modules, content_type=4)
        else:
            homeworks = Contents.objects.filter(lesson__module__in=modules, content_type=4)
        dct['homeworks'] = len(homeworks)
        dct['unseen'] = len(Homeworks.objects.filter(content__in=homeworks, status=1))
        dct['unchecked'] = len(Homeworks.objects.filter(content__in=homeworks, status=2, last_res=True))
        dct['checked'] = len(Homeworks.objects.filter(content__in=homeworks, status=3, last_res=True))
        dct['rejected'] = len(Homeworks.objects.filter(content__in=homeworks, status=4, last_res=True))
        data.append(dct)

    return data


def get_groups_via_hws(courses, user:CustomUser):
    if type(courses) not in [set, list, QuerySet]:
        return []
    data = list()

    groups = Group.objects.filter(course__in=courses)
    if user.is_superuser is False and user.teacher_set.first():
        query = Q(teacher=user.teacher_set.first())|Q(trainer=user.teacher_set.first())
        groups = groups.filter(query)
    
    admins = CustomUser.objects.filter(is_superuser=True)
    for group in groups:
        dct = model_to_dict(group, fields=('id', 'title',))
        if group.teacher:
            dct['teacher'] = group.teacher.user.full_name()
        dct['students'] = len(group.students.all())
        dct['course'] = group.course.title
        modules = group.course.modules.all()
        homeworks = Contents.objects.filter(Q(author=user)|Q(author__in=admins), lesson__module__in=modules, content_type=4, groups__in=[group])
        dct['homeworks'] = len(homeworks)
        dct['unseen'] = len(Homeworks.objects.filter(content__in=homeworks, status=1, last_res=True))
        dct['unchecked'] = len(Homeworks.objects.filter(content__in=homeworks, status=2, last_res=True))
        dct['checked'] = len(Homeworks.objects.filter(content__in=homeworks, status=3, last_res=True))
        dct['rejected'] = len(Homeworks.objects.filter(content__in=homeworks, status=4, last_res=True))
        data.append(dct)
    return data

def get_students_data(group:Group):
    students = GroupStudents.objects.filter(group=group).annotate(
        full_name=Concat(F('student__user__first_name'),Value(' '),F('student__user__last_name')),
    ).values('id', 'student_id', 'full_name')

    for student in list(students):
        student['last_homework'] = Homeworks.objects.filter(student_id=student['student_id']).order_by('date_created').last()
        if student['last_homework']:
            student['last_homework'] = student['last_homework'].status
        else:
            student['last_homework'] = 1
    return students


def get_contents(course, content_type):
    modules = course.modules.all()
    contents = Contents.objects.filter(lesson__module__in=modules,content_type=content_type)

    return contents