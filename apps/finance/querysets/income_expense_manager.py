from django.db.models import QuerySet, Manager, F, Value, Subquery, OuterRef, Sum
from django.db.models.functions import JSONObject
from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.postgres.expressions import ArraySubquery
from django.utils import timezone


from finance.chooses import INCOME_EXPENSE_TYPE, INCOME_EXPENSE_CATEGORY


class IncomeExpenseQuerySet(QuerySet):
    def get_info(self):
        return self.all()

    def objects(self, **kwargs):
        return self.get_info().values(
            'id', 
            'title', 
            'created', 
            'author' 
        ).annotate(
            type_name = dict(INCOME_EXPENSE_TYPE)[F('type')],
            category_name = dict(INCOME_EXPENSE_CATEGORY)[F('category')],
        ).filter(**kwargs)

    def by_category(self, category: int, **kwargs):
        from ..models import IEField
        fields = IEField.fields.fields(type_id=OuterRef('id')).values(
            json=JSONObject(id='id', title='title', type='type', records='records')
        )
        return self.get_info().values(
            'id', 
            'title',
            'type', 
        ).annotate(
            fields = ArraySubquery(fields)
        ).filter(
            category=category,
            **kwargs
        )
    
    def by_type(self, type: int, *kwargs):
        return self.get_info().values(
            'id', 
            'title', 
            'created', 
            'author',
            'type',
        ).filter(type=type, **kwargs)

    # def reports(self):
    #     return self.get_info().filter(
    #         created__gte = timezone.now() - timezone.timedelta(days=365)
    #     ).aggregate(
    #         jan = Sum()
    #     )

class IncomeExpenseManager(Manager):
    def get_queryset(self):
        return IncomeExpenseQuerySet(self.model)
    
    def objects(**kwargs):
        return self.get_queryset().objects(**kwargs)
    
    def by_category(self, cat: int, **kwargs):
        return self.get_queryset().by_category(cat, **kwargs)
    
    def by_type(self, type: int, **kwargs):
        return self.get_queryset().by_type(type, **kwargs)