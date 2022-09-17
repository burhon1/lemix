from django.db.models import Value,Prefetch, Case, When,F,Manager,Func,IntegerField,Q,TextField,Exists,OuterRef
from django.db.models.functions import Concat,Substr,Cast
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet

class StudentQueryset(QuerySet):
    def get_info(self):
        if not self.exists():
            return self.all()
        return self.values(
            'id',
            'user__first_name',
            'user__last_name',
        ).annotate(
            full_name=Concat(F('user__first_name'),Value(' '),F('user__last_name'))
        )

    def students(self):
        return self.get_info()

    def students_attendace(self,id):
        return self.get_info().filter(group__id=id).values(
            'id',
            'full_name'
        ).annotate(
            attendace_status=ArrayAgg(
                Cast('attendace__status', TextField()),
                filter=Q(attendace__status__isnull=False
            ))
        ).annotate(
            attendace=ArrayAgg(
                Cast('attendace__date', TextField()),
                filter=Q(attendace__date__isnull=False
            )),
        )

    def student_balances(self,id):
        return self.get_info().filter(group__id=id).values(
            'id',
            'full_name',
            'payment__paid',
            'payment__created',
            'payment__paid',
            'attendace__date'
            ).annotate(
                attendaces=ArrayAgg(Cast('attendace__date', TextField()),distinct=True)
            )

class StudentManager(Manager):
    def get_query_set(self):
        return StudentQueryset(self.model)
    
    def students(self):
        return self.get_query_set().students() 

    def students_attendace(self,id):
        return self.get_query_set().students_attendace(id)
        
    def student_balances(self,id):
        return self.get_query_set().student_balances(id)