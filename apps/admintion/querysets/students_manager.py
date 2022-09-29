from django.db.models import Value,CharField, Count, When,F,Manager,Func,IntegerField,Q,TextField,Exists,OuterRef, Sum
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
        return self.get_info().values(
            'id',
            'user__first_name',
            'user__last_name',
            'user__phone',
            # 'groups',
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
            group_count = Count(F('ggroups'), distinct=True),
            payment = Sum(F('payment__paid'), distinct=True),
            attendace = ArrayAgg(F('ggroups__attendance'), distinct=True)
        )

    def students_attendace(self,id):
        return self.get_info().filter(ggroups__group__id=id).values(
            'id',
            'full_name'
        ).annotate(
            attendace_status=ArrayAgg(
                Cast('ggroups__attendance__status', TextField()),
                filter=Q(ggroups__attendance__status__isnull=False
            ))
        ).annotate(
            attendace=ArrayAgg(
                Cast('ggroups__attendance__date', TextField()),
                filter=Q(ggroups__attendance__date__isnull=False
            )),
        )

    def student_balances(self,id):
        return self.get_info().filter(ggroups__id=id).values(
            'id',
            'full_name',
            'payment__paid',
            'payment__created',
            'payment__paid',
            #'attendace__date'
            ).annotate(
                attendaces=ArrayAgg(Cast('ggroups__attendance__date', TextField()),distinct=True)
            )

    def students_by_status(self, status: int=1):
        return self.get_info().filter(status=status)
    
    def student_detail(self, id: int):
        return self.get_info().values(
            'id',
            'groups',
            'status',
            'source',
            'comment',
            'user__first_name', 'user__last_name', 'user__middle_name'
        ).annotate(
            full_name = Concat(F('user__last_name'),Value(' '),F('user__first_name')),
            phone_number = Concat(
                Value('+998'), F('user__phone')),
            gender = F('user__gender'),
            birthday = F('user__birthday'),
            location = F('user__location'),
            payment = Sum(F('payment__paid'), distinct=True),
            picture = F('user__picture'),
        ).filter(id=id).first()

    def setudent_list(self):
        return self.get_info().filter(status=True).values('id','full_name')


class StudentManager(Manager):
    def get_query_set(self):
        return StudentQueryset(self.model)
    
    def students(self):
        return self.get_query_set().students() 

    def students_attendace(self,id):
        return self.get_query_set().students_attendace(id)
        
    def student_balances(self,id):
        return self.get_query_set().student_balances(id)

    def student_detail(self, id):
        return self.get_query_set().student_detail(id)

    def studet_list(self):
        return self.get_query_set().setudent_list()  
