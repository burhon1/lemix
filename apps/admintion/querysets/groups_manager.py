from django.db.models import Value, Case, When,F,Manager,Func,IntegerField,CharField,TextField,Exists,OuterRef,Count
from django.contrib.postgres.aggregates import ArrayAgg
# from django.contrib.postgres.functions import ToArray
from django.db.models.functions import Concat,Substr,Cast
from django.db.models.query import QuerySet

# from admintion.models import Student

class GroupQueryset(QuerySet):
    def get_info(self):
        datas = None
        if  not self.exists():
            datas = self.all()
        else:    
            datas = self.values(
                'id',
                'course__title',
                'teacher__user__first_name',
                'teacher__user__last_name',
                'start_time',
                'end_time',
                'course__price',
                'title',
                'room__title',
                'start_date',
                'limit',
            ).annotate(
                course=F("course__title"),
                teacher=Concat(F('teacher__user__first_name'),Value(' '),F('teacher__user__last_name')),
                times = Concat(Substr(Cast(F('start_time'), TextField()),1,5),Value('-'),Substr(Cast(F('end_time'), TextField()),1,5),output_field=CharField()),
                total_student=Count('students',distinct=True),
                days = ArrayAgg(Cast('days__days', TextField()),distinct=True),
                )
            for item in datas:
                item['days'] = 'as'   
        return datas         
                
    def groups(self):
        if  not self.exists():
            return self.all()
        return self.get_info().values(
                'id',
                'title',
                'course',
                'teacher',
                'times',
                'total_student',
                'course__price',
                'days',
                'limit',
            )

    def group(self,id):
        return self.get_info().values(
                'id',
                'title',
                'course',
                'teacher',
                'times',
                'total_student',
                'course__price',
                'room__title',
                'start_date',
                'days',
                'limit',
                'pay_type', 'status', 'comments'
            ).annotate(
                groupdays = F('days'),
            ).filter(id=id).first()

class GroupManager(Manager):
    def get_query_set(self):
        return GroupQueryset(self.model)        

    def groups(self):
        return self.get_query_set().groups() 

    def group(self,id):
        return self.get_query_set().group(id)     