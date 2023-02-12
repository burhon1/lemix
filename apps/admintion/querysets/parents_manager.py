from django.db.models import Value,CharField, Count, When,F,Manager,Func,IntegerField,Q,TextField,Exists,OuterRef, Sum
from django.db.models.functions import Concat,Substr,Cast
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet

class ParentsQueryset(QuerySet):
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

    def parents(self):
        return self.get_info().values(
            'id',
            'user__first_name',
            'user__last_name',
            'user__phone'
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
            student_count = Count(F('students'), distinct=True)
        )\
        .values(
            'id',
            'full_name',
            'phone_number',
            'student_count',
            'status'
        )
    
    def get_parent(self, student_id):
        return self.get_info().filter(students__id=student_id).values(
           'id',
            'user__first_name',
            'user__last_name',
            'user__phone',
            'telegram',
            'passport'
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
                )
        ).first()

class ParentsManager(Manager):
    def get_query_set(self):
        return ParentsQueryset(self.model)
    
    def parents(self):
        return self.get_query_set().parents()

    def parent(self, student_id):
        return self.get_query_set().get_parent(student_id)