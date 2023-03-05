from django.db.models import Value, Case, When,F,Manager,Func,FloatField,Q,CharField,Exists,OuterRef,Count,Sum
from django.db.models.functions import Concat,Substr,Cast
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet
from django.db.models import Func

class Round2(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'

class LeadFormQueryset(QuerySet):
    def lead_forms(self,educenter_id):
        return self.filter(Q(educenters__id__in=educenter_id)|Q(educenters__isnull=True)).annotate(
            send_count=Count('formlead', distinct=True)
        )\
        .annotate(
            conversion=Cast(Round2(Case(When(seen=0,then=Value(0)),
                            default=(F('send_count')*1.0)/F('seen')*100,
                            output_field=FloatField())), output_field=CharField())
            )\
        .values('id','name','title','link','qrcode','seen','send_count','conversion').order_by('-id')

class LeadFormManager(Manager):
    def get_query_set(self):
        return LeadFormQueryset(self.model) 
    
    def lead_forms(self,educenter_id):
        return self.get_query_set().lead_forms(educenter_id) 