from django.db.models import Value, Case, When,F,Manager
from django.db.models.functions import Concat,Substr
from django.db.models.query import QuerySet

# from admintion.models import EduCenters

class RoomQueryset(QuerySet):
    def get_info(self,educenter_id):
        # educenter_ids = 'admintion.EduCenters'.educenters.educenters()
        # print(educenter_ids)
        # objs = 
        # print(objs|objs.prefetch_related(''))
        return self.filter(educenter__id__in=educenter_id)

    def rooms(self,educenter_id):
        return self.get_info(educenter_id)

class RoomManager(Manager):
    def get_query_set(self):
        return RoomQueryset(self.model)
    
    def rooms(self,educenter_id):
        return self.get_query_set().rooms(educenter_id) 