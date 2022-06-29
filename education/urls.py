from django.urls import path

from education.views import *

app_name = 'education'

urlpatterns = [
    path('test/',test2_view,name='test'),
    path('groups/list/',groups_list_view,name='test'),
    path('courses/list/',courses_list_view,name='course'),
    path('course/<int:id>/detail/',course_detail_view,name='course_detail'),
    path('teacher/<int:id>/detail/',teacher_detail_view,name='teacher_detail'),
]
