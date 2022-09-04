from django.db.models import Value, Case, When,F,Manager
from django.db.models.functions import Concat,Substr
from django.db.models.query import QuerySet

class StudentQueryset(QuerySet):
    def get_info(self):
        return self.all()

    
    def students(self):
        return self.get_info()

class StudentManager(Manager):
    def get_query_set(self):
        return StudentQueryset(self.model)
    
    def students(self):
        return self.get_query_set().students() 