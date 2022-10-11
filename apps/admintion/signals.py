from django.db.models.signals import post_save
from django.dispatch import receiver

from admintion.models import Payment, Student

@receiver(post_save, sender=Payment)
def change_student_balance(sender, instance, created, **kwargs):
    if created:
        student = instance.student
        student.balance += instance.paid
        student.save()