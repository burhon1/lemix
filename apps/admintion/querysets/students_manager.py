from django.db.models import Value,CharField, Count, When,F,Manager,Func,IntegerField,Q,TextField,Exists,OuterRef, Sum
from django.db.models.functions import Concat,Substr,Cast
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet

class StudentQueryset(QuerySet):
    def get_info(self):
        print(self.count)
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
        return self.get_info().values(
            'id',
            'user__first_name',
            'user__last_name',
            'user__phone',
            'groups',
            'status'
        ).annotate(
            full_name = Concat(F('user__last_name'),Value(' '),F('user__first_name')),
            phone_number = Concat(
                Value('+998'),
                Value(' ('),
                Substr(F('user__phone'),1,2),
                Value(') '),
                Substr(F('user__phone'),3,3),
                Value(' '),
                Substr(F('user__phone'),6,2),
                Value(' '),
                Substr(F('user__phone'),8,2)
                ),
            group_count = F('groups__id'),
            payment = Sum(F('payment__paid'), distinct=True),
            attendace = Count(F('attendace'))
        )

    def students_attendace(self,id):
        return self.get_info().filter(groups__id=id).values(
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
        return self.get_info().filter(groups__id=id).values(
            'id',
            'full_name',
            'payment__paid',
            'payment__created',
            'payment__paid',
            'attendace__date'
            ).annotate(
                attendaces=ArrayAgg(Cast('attendace__date', TextField()),distinct=True)
            )
    
    def students_by_status(self, status: int=1):
        return self.get_info().filter(status=status)
    

class StudentManager(Manager):
    def get_query_set(self):
        return StudentQueryset(self.model)
    
    def students(self):
        return self.get_query_set().students() 

    def students_attendace(self,id):
        return self.get_query_set().students_attendace(id)
        
    def student_balances(self,id):
        return self.get_query_set().student_balances(id)