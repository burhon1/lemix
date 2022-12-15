from django.db.models.signals import post_save
from django.dispatch import receiver

from admintion.models import LeadDemo, Payment, Student, Attendace

@receiver(post_save, sender=Payment)
def change_student_balance(sender, instance, created, **kwargs):
    if created:
        student = instance.student
        student.balance += instance.paid
        student.save()


@receiver(post_save, sender=LeadDemo)
def add_attendace_for_lead(sender, instance, created, **kwargs):
    if created:
        Attendace.objects.get_or_create(date=instance.date, lead_demo=instance, status=0)
