from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from admintion.models import (Room,Course,Teacher,Group,Student,GroupsDays,Payment,Attendace, GroupStudents, 
                              Parents, LeadDemo, TaskTypes, Tasks, FormLead,LeadStatus,UserTaskStatus,
                              SmsIntegration,Messages,EduCenters,FormFields, FormUniversalFields,Sources,Contacts,LeadForms,
                              Countries, Regions, Districts, 
                            )
from admintion.resources import admintion as resources

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
admin.site.register(SmsIntegration)
admin.site.register(Messages)
admin.site.register(EduCenters)
@admin.register(FormFields)
class FieldsAdmin(admin.ModelAdmin):
    list_filter = ('leadform',)
admin.site.register(FormUniversalFields)
admin.site.register(Sources)
admin.site.register(LeadForms)
admin.site.register(Contacts)


@admin.register(Countries)
class CountriesAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = resources.CountriesResource

@admin.register(Regions)
class RegionsAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = resources.RegionsResource
@admin.register(Districts)
class DistrictsAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = resources.DistrictsResource