from django.db.models import Value, Case, When,F,Manager,Func,IntegerField,Q,TextField,Exists,OuterRef,Count,Sum
from django.db.models.functions import Concat,Substr,Cast
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet

class LeadQueryset(QuerySet):
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

    def leads(self,educenter_id):
        return self.get_info().filter(educenter__id__in=educenter_id).values(
            'id',
            'user__first_name',
            'user__last_name',
            'user__phone',
            'source__title',
            'status__status',
            'comment',
            'author__first_name',
            'author__last_name',
            'created_at'
        ).annotate(
            full_name = Concat(F('user__last_name'),Value(' '),F('user__first_name')),
            author_name=Concat(F('author__first_name'),Value(' '),F('author__last_name')),
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
        )
    
    def lead_list(self,id):
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
            demo_count = Count(F('demo'), distinct=True),
            payment = Sum(F('payment__paid'), distinct=True),
            attendace = ArrayAgg(F('demo__lead_attendance'), distinct=True)
        )
    def leads_attendace(self,id):
        return self.get_info().filter(demo__group__id=id,activity__lt=3).values(
            'id',
        ).annotate(
            attendace_status=ArrayAgg(
                Cast('demo__lead_attendance__status', TextField()),
                filter=Q(demo__lead_attendance__status__isnull=False
            ))
        ).annotate(
            attendace=ArrayAgg(
                Cast('demo__lead_attendance__date', TextField()),
                filter=Q(demo__lead_attendance__date__isnull=False
            )),
        )

class LeadManager(Manager):
    def get_query_set(self):
        return LeadQueryset(self.model) 
    
    def leads(self,educenter_id):
        return self.get_query_set().leads(educenter_id) 

    def leads_attendace(self,id):
        return self.get_query_set().leads_attendace(id)