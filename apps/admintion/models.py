from datetime import timezone
from django.db import models
from admintion.querysets import rooms_manager,groups_manager
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

class GroupsDays(models.Model):
    days = models.PositiveSmallIntegerField(choices=chooses.GROUPS_DAYS)

class Group(models.Model):
    title = models.CharField(max_length=50)
    comments = models.TextField(default="")
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="teacher")
    trainer = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="trainer")
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    days = models.ManyToManyField(GroupsDays)
    pay_type = models.PositiveSmallIntegerField(choices=chooses.PAY_FORMS)
    status = models.PositiveSmallIntegerField(choices=chooses.GROUPS_STATUS)
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
    group = models.ForeignKey(Group,on_delete=models.CASCADE),
    comment = models.TextField()
    # student = 
    