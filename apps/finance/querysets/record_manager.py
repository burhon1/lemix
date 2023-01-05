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
        return self.get_info().aggregate(
            jan = Sum('value', filter=Q(year=curr_year)&Q(month=1)),
            feb = Sum('value', filter=Q(year=curr_year)&Q(month=2)),
            mar = Sum('value', filter=Q(year=curr_year)&Q(month=3)),
            apr = Sum('value', filter=Q(year=curr_year)&Q(month=4)),
            may = Sum('value', filter=Q(year=curr_year)&Q(month=5)),
            jun = Sum('value', filter=Q(year=curr_year)&Q(month=6)),
            jul = Sum('value', filter=Q(year=curr_year)&Q(month=7)),
            aug = Sum('value', filter=Q(year=curr_year)&Q(month=8)),
            sep = Sum('value', filter=Q(year=curr_year)&Q(month=9)),
            oct = Sum('value', filter=Q(year=curr_year)&Q(month=10)),
            now = Sum('value', filter=Q(year=curr_year)&Q(month=11)),
            dec = Sum('value', filter=Q(year=curr_year)&Q(month=12)),
        )



class RecordManager(Manager):
    def get_queryset(self):
        return RecordQuerySet(self.model)

    def records(self, **kwargs):
        return self.get_queryset().records(**kwargs)