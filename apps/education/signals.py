from django.db.models.signals import pre_save
from django.dispatch import receiver

from admintion.models import Course
from education.models import Modules, Lessons, Contents

@receiver(pre_save, sender=Modules)
def set_module_order(sender, instance, **kwargs):
    if instance and instance.order == 1:
        if instance.course:
            last_module = instance.course.modules.last()
            if last_module:
                instance.order = last_module.order + 1 


@receiver(pre_save, sender=Lessons)
def set_module_order(sender, instance, **kwargs):
    if instance and instance.order == 1:
        if instance.module:
            last_lesson = instance.module.lessons.last()
            if last_lesson:
                instance.order = last_lesson.order + 1


@receiver(pre_save, sender=Contents)
def set_module_order(sender, instance, **kwargs):
    if instance and instance.order == 1:
        if instance.lesson:
            last_content = instance.lesson.contents.last()
            if last_content:
                instance.order = last_content.order + 1