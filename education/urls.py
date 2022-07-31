
from django.urls import path

from education.views import *

app_name = 'education'

urlpatterns = [
    path('test/',test2_view,name='test'),
    path('teachers/',teachers_view,name='teachers'),
    path('courses/list/',courses_list_view,name='courses-list'),
    path('course/<int:id>/detail/',course_detail_view,name='course_detail'),

    path('teacher/<int:id>/detail/',teacher_detail_view,name='teacher_detail'),
    path('employe/<int:id>/detail/',employe_detail_view,name='employe_detail'),
    path('group/<int:id>/detail/',group_detail_view,name='group_detail'),
    path('student/<int:id>/detail/',student_detail_view,name='student_detail'),
    path('parents/<int:id>/detail/',parents_detail_view,name='parents_detail'),


    path('teacher/add/',teacher_add_view,name='courseadd'),
    path('groups/list/',groupslist_view,name='groups-list'),
    path('finance/list/',finance_list_view,name='finance-list'),
    path('rooms/list/',roomslist_view,name='rooms-list'),
    path('employees/list/',employees_view,name='employees-list'),
    path('debt/list/',debt_list_view,name='debt-list'),
    
    path('students/list/',students_list_view,name='students-list'),
    path('parents/list/',parents_list_view,name='parents-list'),
    path('expenses/list/',expenses_list_view,name='expenses-list'),
]
