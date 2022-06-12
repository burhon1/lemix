from django.db import models

from education.chooses import COURSES_CHOICES

# Bu yerda kurslar uchun model yaratilgan
class Course(models.Model):
    title = models.CharField(max_length=100)
    duration = models.DurationField()
    student_count = models.SmallIntegerField()
    price = models.PositiveIntegerField()
    course_type = models.IntegerField(choices=COURSES_CHOICES,blank=True,null=True)
    image = models.ImageField(upload_to ='media/course/',blank=True,null=True)
    comment = models.TextField()

    # objects = CourseManager()

    def __str__(self) -> str:
        return self.title
