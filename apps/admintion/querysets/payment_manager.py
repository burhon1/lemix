from django.db.models import Value, Case, When,F,Manager
from django.db.models.functions import Concat,Substr
from django.db.models.query import QuerySet

class PaymentQueryset(QuerySet):
    def get_info(self):
        return self.all()

    def payments(self):
        return self.get_info()

    def student_payments(self, student_id: int):
        return self.get_info().values(
            'id', 'paid', 'created', 'receiver_id', 'payment_type', 'comment'
        ).annotate(
            receiver = Concat(F('receiver__last_name'), Value(' '), F('receiver__first_name'))
        ).filter(student_id=student_id)

class PaymentManager(Manager):
    def get_query_set(self):
        return PaymentQueryset(self.model)
    
    def payments(self):
        return self.get_query_set().payments().order_by('-created')

    def student_payments(self, student_id: int):
        return self.get_query_set().student_payments(student_id).order_by('-created') 