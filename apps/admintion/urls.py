from django.urls import path

from .views import employes,rooms,courses,teachers,groups,students,forms,leads
app_name = 'admintion'

urlpatterns = [
    path('employees/',employes.employees_view,name='employees'),
    path('employee/<int:id>/detail/',employes.employee_detail_view,name='employee-detail'),
    path('rooms/',rooms.rooms_view,name='rooms'),
    path('courses/',courses.courses_view,name='courses'),
    path('teachers/',teachers.teachers_view,name='teachers'),
    path('teacher/<int:id>/detail/',teachers.teacher_detail_view,name='teacher-detail'),
    path('groups/',groups.groups_view,name='groups'),
    path('group/<int:id>/detail/',groups.group_detail_view,name='group-detail'),
    path('group/change/attendace/',groups.change_attendace_view,name='change-attendace'),
    path('group/change/get-attendace/',groups.get_attendace_view,name='get-attendace'),
    path('students/',students.students_view,name='students'),
    path('forms/',forms.forms_view,name='forms'),
    path('leads/',leads.leads_view,name='lead-list')
]
