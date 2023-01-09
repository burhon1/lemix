from django.db.models import QuerySet, Manager, F, Value, Sum, Q
from django.db.models.functions import Concat
from django.utils import timezone

class RecordQuerySet(QuerySet):
    def get_info(self):
        return self.all()

    def records(self, **kwargs):
        return self.get_info().values(
            'id',
            'year',
            'month',
            'value',
            'field_id',
            'created',
            # 'author_id',
        ).annotate(
            # author = Concat(F('author__last_name'), Value(' '), F('author__first_name')),
            field = F('field__title'),
        ).filter(**kwargs)

    def statistics(self, **kwargs):
        curr_year: int = timezone.now().year 
        return self.get_info().all(
           
        ).aggregate(
            jan = Sum('value', filter=Q(year=curr_year)&Q(month=1), default=0),
            feb = Sum('value', filter=Q(year=curr_year)&Q(month=2), default=0),
            mar = Sum('value', filter=Q(year=curr_year)&Q(month=3), default=0),
            apr = Sum('value', filter=Q(year=curr_year)&Q(month=4), default=0),
            may = Sum('value', filter=Q(year=curr_year)&Q(month=5), default=0),
            jun = Sum('value', filter=Q(year=curr_year)&Q(month=6), default=0),
            jul = Sum('value', filter=Q(year=curr_year)&Q(month=7), default=0),
            aug = Sum('value', filter=Q(year=curr_year)&Q(month=8), default=0),
            sep = Sum('value', filter=Q(year=curr_year)&Q(month=9), default=0),
            oct = Sum('value', filter=Q(year=curr_year)&Q(month=10), default=0),
            now = Sum('value', filter=Q(year=curr_year)&Q(month=11), default=0),
            dec = Sum('value', filter=Q(year=curr_year)&Q(month=12), default=0),
        )
 


class RecordManager(Manager):
    def get_queryset(self):
        return RecordQuerySet(self.model)

    def records(self, **kwargs):
        return self.get_queryset().records(**kwargs)

    def statistics(self):
        return self.get_queryset().statistics()