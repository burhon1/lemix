from django.urls import path

from . import views

app_name = 'student'

urlpatterns = [
    path('', views.student_view, name='student'),
    path('<int:pk>/detail/', views.student_detail_view, name='student_detail'),
    path('courses/', views.courses_view, name='courses'),
    path('courses/modules/', views.contents_view, name='contents'),
    path('rating/', views.rating_view, name='rating'),
    path('exams/', views.exams_view, name='exams'),
    path('lesson_detail/', views.lesson_detail_view, name='lesson'),
    path('courses/modules/test/', views.test_view, name='test'),
    path('courses/modules/hometask/', views.homework_detail_view, name='module_hometask'),
    path('homeworks/', views.homework_view, name='homeworks'),
    path('guidance/', views.help_view, name='help'),
]
