from django.db.models import Value, F,Manager
from django.db.models.functions import Concat
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet


class TestsQueryset(QuerySet):
    def get_info(self):
        if not self.exists():
            return self.all()
        return self.values(
            'id',
            'course', 'count_per_student', 
            'lesson', 'module'
        )

    def tests(self):
        return self.get_info()

    def test(self, id: int):
        return self.get_info().filter(id=id).first()


class TestsManager(Manager):
    def get_query_set(self):
        return TestsQueryset(self.model)

    def tests(self):
        return self.get_query_set().tests()

    def test(self, id: int):
        return self.get_query_set().test(id)