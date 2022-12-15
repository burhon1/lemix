from curses import def_shell_mode
from django.db.models import Value, F,Manager
from django.db.models.functions import Concat
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet


class ModulesQueryset(QuerySet):
    def get_info(self):
        if not self.exists():
            return self.all()
        return self.values(
            'id',
            'title', 'course__title', 'order', 
            'author__last_name', 'author__first_name',
        ).annotate(
            full_name=Concat(F('author__first_name'),Value(' '),F('author__last_name'))
        )

    def modules(self):
        return self.get_info()

    def module(self, id: int):
        return self.get_info().values(
                'id', 'title', 'order',
                'course_id', 'course__title', 
                'author__last_name', 'author__first_name',
                'lessons',
            ).annotate(
                author=Concat(F('author__last_name'),Value(' '),F('author__first_name'))
            ).filter(id=id).first()

    def course_modules(self, course_id: int):
        return self.get_info().values(
            'id', 
            'title',
            'order',
            'course',
        ).annotate(
            author = Concat(F('author__last_name'), Value(' '), F('author__first_name')),
            lessons = ArrayAgg(F('lessons'), distinct=True)
        ).filter(course_id=course_id).order_by('order')

class ModulesManager(Manager):
    def get_query_set(self):
        return ModulesQueryset(self.model)

    def modules(self):
        return self.get_query_set().modules()

    def module(self, id: int):
        return self.get_query_set().module(id)

    def course_modules(self, course_id: int):
        return self.get_query_set().course_modules(course_id)