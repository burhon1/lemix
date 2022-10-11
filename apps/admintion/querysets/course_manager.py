from django.db.models import Value, Case, When,F,Manager, TextField, CharField
from django.db.models.functions import Cast, Concat, Substr
from django.db.models.query import QuerySet
from django.contrib.postgres.aggregates import ArrayAgg

class CoursesQueryset(QuerySet):
    def get_info(self):
        return self.all()

    def courses(self):
        return self.get_info()

    def course(self, id):
        return self.get_info().values(
            'id', 
            'title', 
            'comment',
            'status'
            ).filter(id=id).first()

class CoursesManager(Manager):
    def get_query_set(self):
        return CoursesQueryset(self.model)
    
    def courses(self):
        return self.get_query_set().objects()

    def course(self, id):
        return self.get_query_set().course(id)