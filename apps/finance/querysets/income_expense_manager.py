from django.db.models import QuerySet, Manager, F, Value
from django.contrib.postgres.aggregates import ArrayAgg
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
        return self.get_info().values(
            'id', 
            'title', 
            'created', 
            'author',
            'category', 'type',
        ).filter(
            **kwargs
        ).prefetch_related(
            'fields'
        )
    
    def by_type(self, type: int, *kwargs):
        return self.get_info().values(
            'id', 
            'title', 
            'created', 
            'author',
            'type',
        ).filter(**kwargs)


class IncomeExpenseManager(Manager):
    def get_queryset(self):
        return IncomeExpenseQuerySet(self.model)
    
    def objects(**kwargs):
        return self.get_queryset().objects(**kwargs)
    
    def by_category(self, cat: int, **kwargs):
        return self.get_queryset().by_category(cat, **kwargs)
    
    def by_type(self, type: int, **kwargs):
        return self.get_queryset().by_type(type, **kwargs)