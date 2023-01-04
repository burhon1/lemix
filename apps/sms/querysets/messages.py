from django.db.models import QuerySet, F, Value, Manager
from django.db.models.functions import Concat, Substr


class SMSMessageQuerySet(QuerySet):
    def get_info(self):
        return self.all()

    def messages(self, **filter_kwargs):
        return self.get_info().values(
            'id',
            'soums',
            'created_at',
            'sms_count',
            'type',
            'who_sent'
        ).annotate(
            sender = Concat(F('who_sent__last_name'), Value(' '), F('who_sent__first_name')),
            name = Concat(Substr(F('message'), 1, 25), Value('...')),
        ).filter(**filter_kwargs)

    def message(self, **filter_kwargs):
        return self.get_info.values(
            'id',
            'soums',
            'dispatch_id',
            'created_at',
            'sms_count',
            'timedelta',
            'phone_number',
            'country',
            'status',
            'dispatch_id'
        ).filter(**filter_kwargs).first()


class SMSMessageManager(Manager):
    def get_queryset(self):
        return SMSMessageQuerySet(self.model)
    
    def messages(self, **filter_kwargs):
        return self.get_queryset().messages(**filter_kwargs)

    def message(self, **filter_kwargs):
        return self.get_queryset().message(**filter_kwargs)
    