from django.db.models import Value, Case, When,F,Manager,Func,IntegerField,Q,TextField,Exists,OuterRef
from django.db.models.functions import Concat,Substr,Cast
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet

class AttendaceQueryset(QuerySet):
    def get_info(self):
        if not self.exists():
            return self.all()
        return self.values(
        'student__id',
        'student__user__first_name',
        'student__user__last_name',
    )

    def attendaces(self,id):
        return self.get_info().filter(student__group__id=id).annotate(
        id=F('student__id'),
        full_name=Concat(F('student__user__first_name'),Value(' '),F('student__user__last_name')),
        date=ArrayAgg(
                Cast('date', TextField()),
                filter=Q(date__isnull=False
            )),
        status=ArrayAgg(
                Cast('status', TextField()),
                filter=Q(status__isnull=False
            ))  
    ).values(
        'id',
        'status',
        'full_name',
        'date'
    )

class AttendaceManager(Manager):
    def get_query_set(self):
        return AttendaceQueryset(self.model)
    
    def attendaces(self,id):
        return self.get_query_set().attendaces(id) 