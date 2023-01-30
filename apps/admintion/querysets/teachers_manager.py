from django.db.models import Value, Count, When,Case,F,Q,Manager,Func,Subquery,CharField,TextField,Exists,OuterRef
from django.contrib.postgres.aggregates import ArrayAgg
# from django.contrib.postgres.functions import ToArray
from django.db.models.functions import Concat,Substr,Cast
from django.db.models.query import QuerySet


class TeacherQueryset(QuerySet):
    def get_info(self,educenter_id):
            return self.filter(educenter__id__in=educenter_id).annotate(
            full_name=Concat(F('user__first_name'),Value(' '),F('user__last_name')),
            phone_number=Concat(
                Value('+998'),
                Value(' ('),
                Substr(F('user__phone'),1,2),
                Value(') '),
                Substr(F('user__phone'),3,3),
                Value(' '),
                Substr(F('user__phone'),6,2),
                Value(' '),
                Substr(F('user__phone'),8,2)
                ),
            groups=Count(F('group_teacher'))
        )

    def teachers(self,educenter_id):
        return self.get_info(educenter_id).annotate(
            teacher_type=Case(
                When(teacer_type=True,then=Value('O\'qituvchi')),
                default=Value('Yordamchi(support)')
            )
        ).values(
            'id',
            'full_name',
            'phone_number',
            'groups',
            'status',
            'teacer_type',
            'teacher_type'
        )

    def teacher(self,id):
        return self.teachers().filter(id=id).annotate(
            first_name=F('user__first_name'),
            last_name=F('user__last_name'),
            birthday=F('user__birthday'),
            location=F('user__location'),
            students=Count(F('group_teacher__student'))
        ).first() 

    def teacher_list(self,educenter_id):
        return self.get_info(educenter_id).values('id','full_name')

class TeacherManager(Manager):
    def get_query_set(self):
        return TeacherQueryset(self.model)

    def teachers(self,educenter_id):
        return self.get_query_set().teachers(educenter_id)  

    def teacher_list(self,educenter_id):
        return self.get_query_set().teacher_list(educenter_id)    

    def teacher(self,id):
        return self.get_query_set().teacher(id)  
