from django.db import models
from user.models import CustomUser

from education.models import Tests, Questions, Answers, Contents
from student.data import choices

class Homeworks(models.Model):
    student = models.ForeignKey("admintion.Student", models.CASCADE)
    content = models.ForeignKey(Contents, models.CASCADE, related_name='homeworks')
    file    = models.FileField(upload_to="student/homeworks", null=True, blank=True)
    text    = models.TextField("O'quvchining javobi", max_length=5000, blank=True)
    ball    = models.CharField("Uy vazifasi uchun qo'yilgan baho", null=True, blank=True, max_length=10)
    date_created  = models.DateTimeField(auto_now_add=True, editable=True)
    date_modified = models.DateTimeField(auto_now=True, editable=True)
    comment_file  = models.FileField(upload_to="student/homeworks/comments", null=True, blank=True)
    comment = models.TextField("O'quvchiga xabar", max_length=5000, blank=True)
    status  = models.PositiveSmallIntegerField("Uy vazifasining statusi", choices=choices.HOMEWORK_STATUS, default=1)
    commented = models.ForeignKey(CustomUser, models.SET_NULL, null=True)
    last_res  = models.BooleanField("Bu o'quvchining oxirgi javobimi?", default=True)
    class Meta:
        verbose_name = "Uy vazifasi"
        verbose_name_plural = "Uy vazifalari"

class TestResults(models.Model):
    student = models.ForeignKey("admintion.Student", models.CASCADE)
    test    = models.ForeignKey(Tests, models.CASCADE)
    ball    = models.PositiveIntegerField("O'quvchining bahosi", null=True)
    date_created  = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Test Natijasi"
        verbose_name_plural = "Test Natijalari"


class StudentAnswers(models.Model):
    student     = models.ForeignKey("admintion.Student", models.CASCADE)
    test_result = models.ForeignKey(TestResults, models.CASCADE)
    question    = models.ForeignKey(Questions, models.CASCADE)
    answer      = models.ForeignKey(Answers, models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "O'quvchining javobi"
        verbose_name_plural = "O'quvchilarning javoblari"
        unique_together = ('student', 'test_result', 'question')