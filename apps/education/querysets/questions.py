from django.db.models import Value, F,Manager
from django.db.models.functions import Concat
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet


class QuestionsQueryset(QuerySet):
    def get_info(self):
        if not self.exists():
            return self.all()
        return self.values(
            'id',
            'course', 'ball', 
            'question', 'author',
            'answers',
        ).annotate(
            author = Concat(F('author__last_name'),Value(' '),F('author__first_name')),
        )

    def questions(self):
        return self.get_info()

    def question(self, id: int):
        return self.get_info().filter(id=id).first()


class QuestionsManager(Manager):
    def get_query_set(self):
        return QuestionsQueryset(self.model)

    def questions(self):
        return self.get_query_set().questions()

    def question(self, id: int):
        return self.get_query_set().question(id)