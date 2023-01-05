from django.urls import path,include

from .views import student_paid,billing,reports
app_name = 'finance'

urlpatterns = [
    path('student/<int:id>/pay/',student_paid.student_pay,name='student-pay'),
    path('group/pay/',student_paid.group_students_pay,name='group-pay'),
    path('reports/', reports.financial_reports, name='reports'),
    path('click/',student_paid.paid_service,name='paid-services'),
    path('paid-success/',student_paid.paid_success,name='paid-success')
    # path('paycom/intech/', include("payme.urls")),
    # path('paycom/<int:id>/list/', student_paid.check_paid),
]