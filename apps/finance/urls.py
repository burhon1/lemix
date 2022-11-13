from django.urls import path

from .views import student_paid
app_name = 'finance'

urlpatterns = [
    path('student/<int:id>/pay/',student_paid.student_pay,name='student-pay'),
    path('group/pay/',student_paid.group_students_pay,name='group-pay')
]