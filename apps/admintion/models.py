from django.db import models
from admintion.querysets import rooms_manager

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

class Group(models.Model):
    title = models.CharField(max_length=50)
