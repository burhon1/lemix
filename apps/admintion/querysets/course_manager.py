from django.db.models import Value, Case, When,F,Manager, TextField, CharField
from django.db.models.functions import Cast, Concat, Substr
from django.db.models.query import QuerySet
from django.contrib.postgres.aggregates import ArrayAgg

class CoursesQueryset(QuerySet):
    def get_info(self,educenter_id):
        return self.filter(educenter__id__in=educenter_id)

    def courses(self, educenter_id,short_info=False):
        if short_info:
            return self.get_info(educenter_id).values('id', 'title')
        return self.get_info(educenter_id)

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
    
    def courses(self,educenter_id, short_info=False):
        return self.get_query_set().courses(educenter_id,short_info=short_info)

    def course(self, id):
        return self.get_query_set().course(id)