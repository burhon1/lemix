from calendar import Calendar
from datetime import timezone
from django.db import models
from admintion.querysets import rooms_manager,groups_manager,students_manager,attendace_manager,teachers_manager
from admintion.data import chooses
from user.models import CustomUser

# Create your models here.
class Room(models.Model):
    title = models.CharField(max_length=50)
    capacity = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='user/',null=True,blank=True)
    status = models.BooleanField(default=False)

    rooms = rooms_manager.RoomQueryset()

    def __str__(self) -> str:
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    lesson_duration = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    comment = models.TextField()
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class Teacher(models.Model):
    teacer_type = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    status = models.BooleanField(default=False,null=True,blank=True)
    teachers = teachers_manager.TeacherManager()
    objects = models.Manager()

class GroupsDays(models.Model):
    days = models.PositiveSmallIntegerField(choices=chooses.GROUPS_DAYS)

class Group(models.Model):
    title = models.CharField(max_length=50)
    comments = models.TextField(default="")
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="group_teacher")
    trainer = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="trainer")
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    days = models.ManyToManyField(GroupsDays)
    pay_type = models.PositiveSmallIntegerField(choices=chooses.PAY_FORMS)
    status = models.PositiveSmallIntegerField(choices=chooses.GROUPS_STATUS)
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(auto_now=False,auto_now_add=False,null=True, blank=True)
    end_time = models.TimeField(auto_now=False,auto_now_add=False,null=True, blank=True)
    groups = groups_manager.GroupManager()
    objects = models.Manager()

    def __str__(self) -> str:
        return self.title

class Student(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    status = models.BooleanField(default=False,null=True,blank=True)
    source = models.PositiveSmallIntegerField(choices=chooses.STUDENT_SOURCES)
    groups = models.ManyToManyField(Group,related_name='student')
    comment = models.TextField()
    students =  students_manager.StudentManager()
    objects = models.Manager()

class Attendace(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='attendace')
    status = models.SmallIntegerField(choices=chooses.STUDENT_ATTANDENCE_TYPE,null=True,blank=True)
    date = models.DateField()
    objects = models.Manager()
    attendaces = attendace_manager.AttendaceManager()


class Payment(models.Model):
    paid = models.PositiveIntegerField()
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='payment')
    created = models.DateTimeField(auto_now_add=True)

class FormLead(models.Model):
    fio = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    source = models.PositiveSmallIntegerField(choices=chooses.STUDENT_SOURCES)
    status = models.PositiveSmallIntegerField(choices=chooses.LEAD_FORM_STATUS,null=True,blank=True)
    comment = models.TextField()

    def __str__(self) -> str:
        return self.fio
