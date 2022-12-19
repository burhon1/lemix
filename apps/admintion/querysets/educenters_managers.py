from django.db.models.query import QuerySet
from django.db.models import Manager, Value, F  
from django.db.models.functions import Concat
class EduCentersQuerySet(QuerySet):
    def get_info(self):
        return self.all()

    def objects(self):
        return self.get_info()
        
    def educenters(self):
        return self.get_info().values(
            'id',
            'name',
            'address',
            'max_groups',
            'max_students',
            'teacher_can_see_payments',
            'teacher_can_sign_contracts',
            'director_id', 'parent', 'max_groups', 'max_students', 
            'country', 'region_id', 'district_id',
        ).annotate(
            full_name=Concat(F('director__first_name'),Value(' '),F('director__last_name')),
            phone=Concat(Value('+998'),F('director__phone')),
            region=F('region__name'),
            district=F('district__name'),
        )

    def educenter(self, id):
        return self.educenters().filter(pk=id).first()

class EduCentersManager(Manager):
    def get_query_set(self):
        return EduCentersQuerySet(self.model)

    def educenters(self):
        return self.get_query_set().educenters()
    
    def educenter(self, id):
        return self.get_query_set().educenter(id)