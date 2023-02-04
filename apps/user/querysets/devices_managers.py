from django.db.models import QuerySet, F, Value, Manager
from django.db.models.functions import Concat


class DevicesQuerySet(QuerySet):
    def get_info(self):
        return self.all()

    def objects(self):
        return self.get_info().values(
            'id',
            'ip',
            'device',
            'connected',
            'status',
            'mac_address'
        ).annotate(
            full_name=Concat('user__first_name', Value(' '), 'user__last_name'),
        )


    def filtr(self, **kwargs):
        return self.filter(**kwargs)


class DeviceManager(Manager):
    def get_query_set(self):
        return DevicesQuerySet(self.model)

    def filter(self, **kwargs):
        return self.get_query_set().filtr(**kwargs)