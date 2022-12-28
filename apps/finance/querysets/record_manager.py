from django.db.models import QuerySet, Manager, F, Value
from django.db.models.functions import Concat


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
            'author_id',
        ).annotate(
            author = Concat(F('author__last_name'), Value(' '), F('author__first_name')),
            field = F('field__title'),
        ).filter(**kwargs)


class RecordManager(Manager):
    def get_queryset(self):
        return RecordQuerySet(self.model)

    def records(self, **kwargs):
        return self.get_queryset().records(**kwargs)