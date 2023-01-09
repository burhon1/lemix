from django.db.models import QuerySet, Manager, F, Value, OuterRef
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models.functions import Concat, JSONObject


class FieldQuerySet(QuerySet):
    def get_info(self):
        return self.all()

    def fields(self, **kwargs):
        from finance.models import IERecord
        records = IERecord.records.records(field_id=OuterRef('pk')).values(
            json=JSONObject(id='id', month='month', value='value', year='year')
        )
        return self.get_info().values(
            'id',
            'title',
            'type_id',
            'is_active',
            'created',
            'author_id',
        ).annotate(

            # type = F('type__title'),
            author = Concat(F('author__last_name'), Value(' '), F('author__first_name')),
            # records_soums = Sum()
            records = ArraySubquery(records)
        ).filter(**kwargs)

    def field(self, id: int):
        return self.fields(id=id).first()


class FieldManager(Manager):
    def get_queryset(self):
        return FieldQuerySet(self.model)
    
    def fields(self, **kwargs):
        return self.get_queryset().fields(**kwargs)

    def field(self, id: int):
        return self.get_queryset().field(id=id)