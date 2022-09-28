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
    path('group/<int:id>/data/',groups.group_detail_data,name='group-data'),
    path('group/change/attendace/',groups.change_attendace_view,name='change-attendace'),
    path('group/change/get-attendace/',groups.get_attendace_view,name='get-attendace'),
    path('students/',students.students_view,name='students'),
    path('student/<int:id>/detail/',students.student_detail_view,name='student-detail'),
    path('student/<int:id>/delete/',students.student_delete_view,name='student-delete'),
    path('student/<int:id>/add-group/', students.student_add_group_view, name='add-student-to-group'),
    path('student/<int:id>/deactivate-in-group/', students.student_deactivate_view, name='deactivate-student-in-group'),
    path('student/<int:id>/remove-in-group/', students.student_remove_view, name='remove-student-in-group'),
    path('student/<int:id>/activate-in-group/', students.student_activate_view, name='activate-student-in-group'),
    path('forms/',forms.forms_view,name='forms'),
    path('leads/',leads.leads_view,name='lead-list')
]
