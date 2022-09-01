from django.urls import path

from .views import employes,rooms,courses,teachers,groups,students
app_name = 'admintion'

urlpatterns = [
    path('employees/',employes.employees_view,name='employees'),
    path('employee/<int:id>/detail/',employes.employee_detail_view,name='employee-detail'),
    path('rooms/',rooms.rooms_view,name='rooms'),
    path('courses/',courses.courses_view,name='courses'),
    path('teachers/',teachers.teachers_view,name='teachers'),
    path('groups/',groups.groups_view,name='groups'),
    path('students/',students.students_view,name='students')
]
