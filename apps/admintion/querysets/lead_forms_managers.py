from django.db.models import Value, Case, When,F,Manager,Func,CharField,Q,TextField,Exists,OuterRef,Count,Sum
from django.db.models.functions import Concat,Substr,Cast
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet

class LeadFormQueryset(QuerySet):
    def lead_forms(self,educenter_id):
        return self.filter(educenters__id__in=educenter_id).annotate(
            send_count=Count('formlead', distinct=True)
        )\
        .annotate(conversion=F('seen')/Value(100.0)*F('send_count'))\
        .values('id','name','title','link','qrcode','seen','send_count','conversion').order_by('-id')

class LeadFormManager(Manager):
    def get_query_set(self):
        return LeadFormQueryset(self.model) 
    
    def lead_forms(self,educenter_id):
        return self.get_query_set().lead_forms(educenter_id) 