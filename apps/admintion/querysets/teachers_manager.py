from django.db.models import Value, Case, When,F,Manager,Func,IntegerField,CharField,TextField,Exists,OuterRef
from django.contrib.postgres.aggregates import ArrayAgg
# from django.contrib.postgres.functions import ToArray
from django.db.models.functions import Concat,Substr,Cast
from django.db.models.query import QuerySet


class TeacherQueryset(QuerySet):

    def teachers(self):
        return self.annotate(
            full_name=Concat(F('user__first_name'),Value(' '),F('user__last_name')),
        ).values(
            'id',
            'full_name'
        )


class TeacherManager(Manager):
    def get_query_set(self):
        return TeacherQueryset(self.model)

    def teachers(self):
        return self.get_query_set().teachers()    
