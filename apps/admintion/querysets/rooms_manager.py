from django.db.models import Value, Case, When,F,Manager
from django.db.models.functions import Concat,Substr
from django.db.models.query import QuerySet

class RoomQueryset(QuerySet):
    def get_info(self):
        return self.all()

    def rooms(self):
        return self.get_info()

class UserManager(Manager):
    def get_query_set(self):
        return RoomQueryset(self.model)
    
    def rooms(self):
        return self.get_query_set().rooms() 