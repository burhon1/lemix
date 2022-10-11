from django.urls import path

from . import views

app_name = 'student'

urlpatterns = [
    path('', views.student_view, name='student'),
    # path('<int:pk>/detail/', views.student_detail_view, name='student_detail'),
    path('my-courses/', views.my_courses_view, name='my-courses'),
    path('my-courses/<int:id>/modules/', views.course_modules_view, name='course-modules'),
    path('exams/<int:pk>/', views.exam_view, name='test'),
    path('my-courses/<int:id>/modules/hometask/', views.homework_detail_view, name='module_hometask'),
    path('rating/', views.rating_view, name='rating'),
    path('exams/', views.exams_view, name='exams'),
    path('homework/<int:pk>/', views.student_homework_view, name='homework'),
    path('<str:type>/<int:pk>/', views.lesson_detail_view, name='lesson'),
    path('homeworks/', views.homeworks_view, name='homeworks'),
    path('guidance/', views.help_view, name='help'),
]
