from django.db import models
from django.core.validators import FileExtensionValidator

from user.models import CustomUser
from education.chooses import COURSES_CHOICES, LESSONS_CHOICES, CONTENT_CHOICES
from admintion.models import Course, FormLead, Student, Group
from education.querysets import modules, lessons, contents, resources, tests, questions, answers

class Modules(models.Model):
    course = models.ForeignKey(Course, models.CASCADE, verbose_name="Kurs", related_name="modules")
    groups = models.ManyToManyField(Group, blank=True)
    title  = models.CharField("Modul sarlavhasi", max_length=300)
    author = models.ForeignKey(CustomUser, models.SET_NULL, null=True)
    order  = models.IntegerField("Dars o'rni", default=0)
    comment= models.TextField(null=True,blank=True)
    objects = models.Manager()
    modules = modules.ModulesManager()
    class Meta:
        verbose_name = "Kurs Moduli"
        verbose_name_plural = "Kurs Modullari"
        ordering = ("order", )
    
    def __str__(self):
        return '%s-%s' %(self.title, self.course.title)

class Lessons(models.Model):
    module = models.ForeignKey(Modules, models.CASCADE, verbose_name="Modul", related_name="lessons")
    groups = models.ManyToManyField(Group, blank=True)
    title  = models.CharField("Mavzu sarlavhasi", max_length=300)
    order  = models.IntegerField("Dars o'rni", default=0)
    content_type = models.SmallIntegerField("Content Type", choices=LESSONS_CHOICES, default=1)
    author = models.ForeignKey(CustomUser, models.SET_NULL, null=True)
    comment= models.TextField(null=True,blank=True)
    objects = models.Manager()
    lessons = lessons.LessonsManager()
    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        ordering = ("order", )

    def __str__(self):
        return '%s-%s' %(self.title, self.module.title)
class Contents(models.Model):
    lesson       = models.ForeignKey(Lessons, models.CASCADE, verbose_name="Dars", related_name="contents")
    groups       = models.ManyToManyField(Group, blank=True)
    title        = models.CharField("Sarlavha", max_length=300)
    content_type = models.SmallIntegerField("Content Type", choices=CONTENT_CHOICES, default=1)
    video        = models.FileField("Video Material", validators=[FileExtensionValidator(['mp4'])], null=True, blank=True)
    video_link   = models.URLField("Video havola", null=True, blank=True)
    text         = models.TextField(null=True, blank=True)
    
    homework     = models.FileField("Uy vazifa uchun topshiriq", null=True, blank=True)

    order        = models.IntegerField("Material o'rni", default=0)
    students     = models.ManyToManyField(Student, verbose_name="Talabalar", blank=True)
    leads        = models.ManyToManyField(FormLead, verbose_name="Lidlar", blank=True)
    opened_at    = models.DateTimeField("O'quvchiga ochilish vaqti",null=True, blank=True)
    closed_at    = models.DateTimeField("Yopilish vaqti",null=True, blank=True)
    author       = models.ForeignKey(CustomUser, models.SET_NULL, null=True)
    required     = models.BooleanField("Dars tugatilmasa keyingi dars ko'rinmasinmi?", default=False)
    status       = models.BooleanField("Material tayyormi? ", default=False)
    objects = models.Manager()
    contents = contents.ContentsManager()
    class Meta:
        verbose_name = "Dars Materiali"
        verbose_name_plural = "Dars Materiallari"
        ordering = ("order", )
 
    def __str__(self):
        return '%s-%s' %(self.title, self.lesson.title)

    @property
    def get_value(self):
        """
        Check function returned value before using it, it may be NoneType, int, str 
        """
        if self.content_type == 1:
            return self.video.url if self.video else self.video_link
        elif self.content_type == 2:
            return self.text
        # elif self.content_type == 3:
        #     return self.tests.all().first() 
        elif self.content_type == 4:
            return self.homework.url if self.homework else self.text

class Resources(models.Model):
    lesson  = models.ForeignKey(Lessons, models.CASCADE, null=True, blank=True, verbose_name="Dars", related_name='resources')
    module  = models.ForeignKey(Modules, models.CASCADE, null=True, blank=True, verbose_name="Modul", related_name='module_resources')
    content = models.ForeignKey(Contents, models.CASCADE, null=True, blank=True, verbose_name="Content", related_name='content_resources')
    file    = models.FileField("Manba", null=True, blank=True)
    link    = models.URLField("Manba havolasi", null=True, blank=True)
    objects = models.Manager()
    resources = resources.ResourcesManager()
    class Meta:
        verbose_name = "Qo'shimcha manbaa"
        verbose_name_plural = "Qo'shimcha manbaalar"


class Tests(models.Model):
    course  = models.ForeignKey(Course, models.SET_NULL, blank=True, null=True)
    module  = models.ForeignKey(Modules, models.SET_NULL, blank=True, null=True)
    lesson  = models.ForeignKey(Lessons, models.SET_NULL, blank=True, null=True)
    count_per_student = models.PositiveIntegerField("1 ta o'quvchi uchun testlar soni", default=0)
    opened_at    = models.DateTimeField("O'quvchiga ochilish vaqti",null=True, blank=True)
    closed_at    = models.DateTimeField("Yopilish vaqti",null=True, blank=True)
    
    objects = models.Manager()
    tests = tests.TestsManager()
    class Meta:
        verbose_name = "Test"
        verbose_name = "Testlar"


class Questions(models.Model):
    question = models.CharField("Test Savoli", max_length=1000)
    author   = models.ForeignKey(CustomUser, models.SET_NULL, null=True)
    test     = models.ForeignKey(Tests, models.CASCADE, related_name='questions')
    ball     = models.FloatField("Ball", default=0, help_text="Savol necha balli?")
    objects = models.Manager()
    questions = questions.QuestionsManager()
    class Meta:
        verbose_name = "Test Savoli"
        verbose_name_plural = "Test Savollari"

class Answers(models.Model):
    question = models.ForeignKey(Questions, models.CASCADE, related_name='answers')
    answer   = models.CharField("Test javobi", max_length=500)
    is_right = models.BooleanField("To'g'ri javobi?")
    objects = models.Manager()
    answers = answers.AnswersManager()
    class Meta:
        verbose_name = "Test javobi"
        verbose_name_plural = "Test javoblari"


class FAQ(models.Model):
    content  = models.ForeignKey(Contents, models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=600)
    answer   = models.CharField(max_length=1500)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"