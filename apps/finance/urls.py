from django.urls import path

from .views import student_paid,billing
app_name = 'finance'

urlpatterns = [
    path('student/<int:id>/pay/',student_paid.student_pay,name='student-pay'),
    path('group/pay/',student_paid.group_students_pay,name='group-pay'),
    path('paycom/intech/', student_paid.TestView.as_view()),
    path('paycom/<int:id>/list/', student_paid.check_paid),
    path('billing/',billing.student_pay),
    path('pay/',student_paid.pay_student),
    path('click/transaction/',student_paid.TestClickView.as_view())
]