from django.db.models import Value, Count, When,Case,F,Q,Manager,Func,Subquery,CharField,TextField,Exists,OuterRef
from django.contrib.postgres.aggregates import ArrayAgg
# from django.contrib.postgres.functions import ToArray
from django.db.models.functions import Concat,Substr,Cast
from django.db.models.query import QuerySet


class TeacherQueryset(QuerySet):

    def teachers(self):
        return self.annotate(
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
        ).annotate(
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


class TeacherManager(Manager):
    def get_query_set(self):
        return TeacherQueryset(self.model)

    def teachers(self):
        return self.get_query_set().teachers()  

    def teacher(self,id):
        return self.get_query_set().teacher(id)  
