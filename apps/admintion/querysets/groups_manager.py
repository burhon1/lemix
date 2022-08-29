from django.db.models import Value, Case, When,F,Manager
from django.contrib.auth.models import BaseUserManager
from django.db.models.functions import Concat,Substr
from django.db.models.query import QuerySet

class GroupQueryset(QuerySet):
    def groups(self):
        return self.annotate(
            ful=Value("")
        )

class GroupManager(Manager):
    def get_query_set(self):
        return GroupQueryset(self.model)        