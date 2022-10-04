from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from tinymce.models import HTMLField

from user.models import CustomUser
from education.chooses import COURSES_CHOICES, LESSONS_CHOICES
from admintion.models import Course, Student
# Bu yerda kurslar uchun model yaratilgan

class Modules(models.Model):
    course = models.ForeignKey(Course, models.CASCADE, verbose_name="Kurs")
    title  = models.CharField("Modul sarlavhasi", max_length=300)
    author = models.ForeignKey(CustomUser, models.DO_NOTHING)
    order  = models.IntegerField("Dars o'rni", default=0)
    class Meta:
        verbose_name = "Kurs Moduli"
        verbose_name_plural = "Kurs Modullari"
        ordering = ("order", )

class Lessons(models.Model):
    module = models.ForeignKey(Modules, models.CASCADE, verbose_name="Modul")
    title  = models.CharField("Modul sarlavhasi", max_length=300)
    order  = models.IntegerField("Dars o'rni", default=0)

    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        ordering = ("order", )

class Contents(models.Model):
    lesson       = models.ForeignKey(Lessons, models.CASCADE, verbose_name="Dars")
    title        = models.CharField("Sarlavha", max_length=300)
    content_type = models.SmallIntegerField("Content Type", choices=LESSONS_CHOICES, default=0)
    video        = models.FileField("Video Material", validators=[FileExtensionValidator(['mp4'])], null=True)
    video_link   = models.URLField("Video havola", null=True)
    text         = HTMLField(null=True)
    # test  = models
    order        = models.IntegerField("Material o'rni", default=0)
    students     = models.ManyToManyField(Student, verbose_name="Talabalar")
    opened_at    = models.DateTimeField("O'quvchiga ochilish vaqti")
    closed_at    = models.DateTimeField("Yopilish vaqti")

    class Meta:
        verbose_name = "Dars Materiali"
        verbose_name_plural = "Dars Materiallari"
        ordering = ("order", )
class Resources(models.Model):
    lesson  = models.ForeignKey(Lessons, models.CASCADE, null=True, verbose_name="Dars")
    module  = models.ForeignKey(Modules, models.CASCADE, null=True, verbose_name="Modul")
    file    = models.FileField("Manba", null=True)
    link    = models.URLField("Manba havolasi", null=True)

    class Meta:
        verbose_name = "Qo'shimcha manbaa"
        verbose_name_plural = "Qo'shimcha manbaalar"


class Tests(models.Model):
    # course = models.ForeignKey(Course, models.SET_NULL, null=True)
    module  = models.ForeignKey(Modules, models.SET_NULL, null=True)
    content = models.ForeignKey(Contents, models.SET_NULL, null=True)
    count_per_student = models.PositiveIntegerField("1 ta o'quvchi uchun testlar soni", default=0)

    class Meta:
        verbose_name = "Test"
        verbose_name = "Testlar"


class Questions(models.Model):
    question = models.CharField("Test Savoli", max_length=1000)
    author   = models.ForeignKey(CustomUser, models.DO_NOTHING, null=True)
    course   = models.ForeignKey(Course, models.SET_NULL, null=True)
    ball     = models.FloatField("Ball", default=0, help_text="Savol necha balli?")

    class Meta:
        verbose_name = "Test Savoli"
        verbose_name_plural = "Test Savollari"

class Answers(models.Model):
    question = models.ForeignKey(Questions, models.CASCADE)
    answer   = models.CharField("Test javobi", max_length=500)
    is_right = models.BooleanField("To'g'ri javobi?")

    class Meta:
        verbose_name = "Test javobi"
        verbose_name_plural = "Test javoblari"
