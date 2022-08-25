from django.urls import path

from .views import employes,rooms,courses
app_name = 'admintion'

urlpatterns = [
    path('employees/',employes.employees_view,name='employees'),
    path('employee/<int:id>/detail/',employes.employee_detail_view,name='employee-detail'),
    path('rooms/',rooms.rooms_view,name='rooms'),
    path('courses/',courses.courses_view,name='courses'),
]
