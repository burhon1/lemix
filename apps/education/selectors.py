from django.utils import timezone 
from user.models import CustomUser
from education.models import Lessons, Modules
from admintion.models import Course, Student

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

def get_lesson_contents_data(lesson_obj: Lessons, student:Student):
    contents = lesson_obj.contents.all()
    data = list()
    for content in contents:
        data.append({
            'id': content.id,
            'title': content.title,
            'content_type': content.content_type,
            'viewed': bool(student in content.students.all()),
            'open': bool(content.opened_at and content.opened_at < timezone.now())
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