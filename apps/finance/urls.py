from django.urls import path,include

from .views import student_paid,billing
app_name = 'finance'

urlpatterns = [
    path('student/<int:id>/pay/',student_paid.student_pay,name='student-pay'),
    path('group/pay/',student_paid.group_students_pay,name='group-pay'),
    # path('paycom/intech/', include("payme.urls")),
    # path('paycom/<int:id>/list/', student_paid.check_paid),
]