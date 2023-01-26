from django.db.models import Value, Case, When,F,Manager,Func,IntegerField,Subquery,CharField,TextField,Exists,OuterRef,Count
from django.contrib.postgres.aggregates import ArrayAgg
# from django.contrib.postgres.functions import ToArray
from django.db.models.functions import Concat,Substr,Cast
from django.db.models.query import QuerySet

# from admintion.models import Student

class GroupQueryset(QuerySet):
    def get_info(self,educenter_id):
        datas = None
        if  not self.exists():
            datas = self.all()
        else:    
            datas = self.filter(educenter__id__in=educenter_id).values(
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
                
    def groups(self, educenter_ids,short_info=False):
        if not self.exists():
            return self.all()
        if short_info:
            columns = (
                'id',
                'title',
                )
        else:
            columns = (
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
        return self.get_info(educenter_ids).values(
                *columns
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


    def pay_by_lesson(self):
        return self.filter(pay_type=1).annotate(
            students=Subquery(
                'admintion.models.Student'.students.filter_by_group(OuterRef('id'))
            )
        )

    def pay_by_month(self):
        return self.filter(pay_type=2) 

    def pay_by_year(self):
        return self.filter(pay_type=3)

    def pay_by_module(self):
        return self.filter(pay_type=4)
                 

class GroupManager(Manager):
    def get_query_set(self):
        return GroupQueryset(self.model)        

    def groups(self,educenter_ids, short_info=False):
        return self.get_query_set().groups(educenter_ids,short_info=short_info) 

    def group_list(self):
        return self.get_query_set().group_list()   

    def group(self,id):
        return self.get_query_set().group(id)  

