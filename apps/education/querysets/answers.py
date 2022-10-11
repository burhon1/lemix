from django.db.models import Value, F,Manager
from django.db.models.functions import Concat
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet


class AnswersQueryset(QuerySet):
    def get_info(self):
        if not self.exists():
            return self.all()
        return self.values(
            'id', 
            'question_id', 'question__question',
            'answer',
        )

    def answers(self):
        return self.get_info()

    def answer(self, id: int):
        return self.get_info().filter(id=id).first()


class AnswersManager(Manager):
    def get_query_set(self):
        return AnswersQueryset(self.model)

    def answers(self):
        return self.get_query_set().answers()

    def answer(self, id: int):
        return self.get_query_set().answer(id)