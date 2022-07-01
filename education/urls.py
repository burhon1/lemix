from django.urls import path

from education.views import *

app_name = 'education'

urlpatterns = [
    path('test/',test2_view,name='test'),
    path('groups/list/',groups_list_view,name='groups-list'),
    path('courses/list/',courses_list_view,name='courses-list'),
    path('course/<int:id>/detail/',course_detail_view,name='course_detail'),

    path('teacher/<int:id>/detail/',teacher_detail_view,name='teacher_detail'),
    path('employe/<int:id>/detail/',employe_detail_view,name='employe_detail'),

    path('teacher/add/',teacher_add_view,name='courseadd'),
    path('guruhlar/',guruhlar_view,name='guruhlar'),
    path('roomslist/',roomslist_view,name='roomslist'),
    path('employees/',employees_view,name='employees'),

]

