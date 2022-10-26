from email.policy import default
from django.db import models
from finance.chooses import *

# Create your models here.
class Paid(models.Model):
    student = models.ForeignKey('admintion.Student',models.CASCADE)
    group = models.ForeignKey('admintion.Group',models.CASCADE,null=True,blank=True)
    paid = models.PositiveBigIntegerField()
    goal_type = models.PositiveSmallIntegerField(choices=GOAL_TYPE)
    paid_type = models.PositiveSmallIntegerField(choices=PAID_TYPE)
    description = models.TextField()
    user = models.ForeignKey('user.CustomUser',models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

class StudentBalance(models.Model):
    title = models.CharField(max_length=100)
    student = models.ForeignKey('admintion.Student',models.CASCADE)
    balance = models.BigIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Talabaning balansi" 
        verbose_name_plural = "Talabaning balanslari"