from django.db.models import Value, Case, When,F,Manager
from django.contrib.auth.models import BaseUserManager
from django.db.models.functions import Concat,Substr
from django.db.models.query import QuerySet

class GroupQueryset(QuerySet):
    def groups(self):
        return self.prefetch_related('student_group').values(
        'course__title',
        'teacher__user__first_name',
        'teacher__user__last_name',
        'course__price',
        'student_group'
        ).annotate(
            course=F("course__title"),
            teacher=Concat(F('teacher__user__first_name'),Value(' '),F('teacher__user__last_name')),
            )

class GroupManager(Manager):
    def get_query_set(self):
        return GroupQueryset(self.model)        

    def groups(self):
        return self.get_query_set().groups()    