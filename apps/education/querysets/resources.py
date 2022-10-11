from django.db.models import Value, F,Manager
from django.db.models.functions import Concat
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet


class ResourcesQueryset(QuerySet):
    def get_info(self):
        if not self.exists():
            return self.all()
        return self.values(
            'id',
            'file', 'link', 
            'lesson', 'module'
        )

    def resources(self):
        return self.get_info()

    def resource(self, id: int):
        return self.get_info().filter(id=id).first()


class ResourcesManager(Manager):
    def get_query_set(self):
        return ResourcesQueryset(self.model)

    def resources(self):
        return self.get_query_set().resources()

    def resource(self, id: int):
        return self.get_query_set().resource(id)