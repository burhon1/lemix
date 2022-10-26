from django.contrib import admin

from admintion.models import Room,Course,Teacher,Group,Student,GroupsDays,Payment,Attendace, GroupStudents, Parents, LeadDemo, TaskTypes, Tasks, FormLead,LeadStatus,UserTaskStatus

# Register your models here.
admin.site.register(Room)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(GroupsDays)
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Payment)
admin.site.register(Attendace)
@admin.register(Parents)
class ParentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)

@admin.register(GroupStudents)
class GroupStudentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'group', 'status')
    list_display_links = ('id', 'student', 'group', 'status')

admin.site.register(LeadDemo)
admin.site.register(TaskTypes)
admin.site.register(Tasks)
admin.site.register(FormLead)
admin.site.register(LeadStatus)
admin.site.register(UserTaskStatus)
