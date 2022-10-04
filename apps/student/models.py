from django.db import models

from education.models import Tests, Question, Answers, Contents


class Homeworks(models.Model):
    student = models.ForeignKey("admintion.Student", models.CASCADE)
    content = models.ForeignKey(Contents, models.CASCADE)
    file    = models.FileField(upload_to="student/homeworks", null=True)
    text    = models.TextField("O'quvchining javobi", max_length=5000)
    ball    = models.SmallIntegerField("Uy vazifasi uchun qo'yilgan baho", null=True)
    date_created  = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

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
    question    = models.ForeignKey(Question, models.DO_NOTHING)
    answer      = models.ForeignKey(Answers, models.DO_NOTHING, null=True)

    class Meta:
        verbose_name = "O'quvchining javobi"
        verbose_name_plural = "O'quvchilarning javoblari"