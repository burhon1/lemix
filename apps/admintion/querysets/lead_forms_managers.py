from django.db.models import Value, Case, When,F,Manager,Func,FloatField,Q,IntegerField,Exists,OuterRef,Count,Sum
from django.db.models.functions import Concat,Substr,Cast
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet
from django.db.models import Func

class Round2(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 0)'

class LeadFormQueryset(QuerySet):
    def lead_forms(self,educenter_id):
        return self.filter(Q(educenters__id__in=educenter_id)|Q(educenters__isnull=True)).annotate(
            send_count=Count('formlead', distinct=True)
        )\
        .annotate(
            conversion=Case(When(seen=0,then=Value(0)),
                            default=(F('send_count')*1.0)/F('seen')*100,
                            output_field=IntegerField())
            ).annotate(
            color=Case(
            When(conversion__lte=29,then=Value('danger')),
            When(conversion__lte=70,then=Value('warning')),
            When(conversion__lte=100,then=Value('success')),
            default=Value('dark')
            )
        ).values('id','name','title','link','qrcode','seen','send_count','conversion','color').order_by('-id')

class LeadFormManager(Manager):
    def get_query_set(self):
        return LeadFormQueryset(self.model) 
    
    def lead_forms(self,educenter_id):
        return self.get_query_set().lead_forms(educenter_id) 