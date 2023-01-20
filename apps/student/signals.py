from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import Homeworks

@receiver(pre_save, sender=Homeworks)
def set_homework_last_status_false(sender, instance, **kwargs):
    last_content = Homeworks.objects.filter(content=instance.content, student=instance.student, status__in=[2, 4]).order_by('date_created')
    if last_content:
        last_content.update(last_res=False)