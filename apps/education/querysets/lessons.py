from django.db.models import Value, F,Manager
from django.db.models.functions import Concat
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet


class LessonsQueryset(QuerySet):
    def get_info(self):
        if not self.exists():
            return self.all()
        return self.values(
            'id',
            'title', 'order', 
            'module_id', 'module__title',
            'content_type', 'contents'
        )

    def lessons(self):
        return self.get_info()

    def lesson(self, id: int):
        return self.get_info().filter(id=id).first()


class LessonsManager(Manager):
    def get_query_set(self):
        return LessonsQueryset(self.model)

    def lessons(self):
        return self.get_query_set().lessons()

    def lesson(self, id: int):
        return self.get_query_set().lesson(id)