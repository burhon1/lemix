from django.contrib import admin

from admintion.models import Room,Course,Teacher,Group,Student,GroupsDays,Payment,Attendace

# Register your models here.
admin.site.register(Room)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(GroupsDays)
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Payment)
admin.site.register(Attendace)