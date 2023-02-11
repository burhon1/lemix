from django.db.models import Value, Case,Count, When,F,Manager
from django.db.models.functions import Concat,Substr
from django.db.models.query import QuerySet

# from admintion.models import EduCenters

class RoomQueryset(QuerySet):
    def get_info(self,educenter_id):
        return self.filter(educenter__id__in=educenter_id)

    def rooms(self,educenter_id):
        return self.get_info(educenter_id)\
            .annotate(
                group_count=Count(F('group'), distinct=True)
            )\
            .order_by('-id')

class RoomManager(Manager):
    def get_query_set(self):
        return RoomQueryset(self.model)
    
    def rooms(self,educenter_id):
        return self.get_query_set().rooms(educenter_id) 