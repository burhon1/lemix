from django.db.models import Value, Case, When,F,Manager,Count,CharField,TextField
from django.contrib.postgres.aggregates import StringAgg
from django.db.models.functions import Concat,Substr,Cast
from django.db.models.query import QuerySet

class GroupQueryset(QuerySet):
    def groups(self):
        return self.values(
            'course__title',
            'teacher__user__first_name',
            'teacher__user__last_name',
            'start_time',
            'end_time',
            'course__price',
            'title'
        ).annotate(
            course=F("course__title"),
            teacher=Concat(F('teacher__user__first_name'),Value(' '),F('teacher__user__last_name')),
            times = Concat(Substr(F('start_time'),1,5),Value('-'),Substr(F('end_time'),1,5),output_field=CharField()),
            ).annotate(
                total_student=Count('student__id'),
                days = StringAgg(Cast('days__days', TextField()),delimiter=',')
                ).values(
                'title',
                'course',
                'teacher',
                'times',
                'total_student',
                'course__price',
                # 'days'
            )

class GroupManager(Manager):
    def get_query_set(self):
        return GroupQueryset(self.model)        

    def groups(self):
        return self.get_query_set().groups()    