from django.db.models import Value, Case, When,F,Manager, TextField, CharField
from django.db.models.functions import Cast, Concat, Substr
from django.db.models.query import QuerySet
from django.contrib.postgres.aggregates import ArrayAgg

class GroupStudentsQueryset(QuerySet):
    def get_info(self):
        return self.all()

    def objects(self):
        return self.get_info()

    def student_groups(self, student_id):
        return self.get_info().values(
            'id', 'group_id', 'group__title', 'status', 'created', 'group__course__price','finished'
        ).annotate(
            days = ArrayAgg(Cast('group__days__days', TextField()),distinct=True),
            course = F('group__course__title'),
            course_id = F('group__course_id'),
            teacher = Concat(F('group__teacher__user__last_name'), Value(' '), F('group__teacher__user__first_name'), output_field=CharField()),
            times = Concat(Substr(Cast(F('group__start_time'), TextField()),1,5),Value('-'),Substr(Cast(F('group__end_time'), TextField()),1,5),output_field=CharField()),
        ).filter(student_id=student_id)

class GroupStudentManager(Manager):
    def get_query_set(self):
        return GroupStudentsQueryset(self.model)
    
    def objects(self):
        return self.get_query_set().objects().order_by('-created')

    def student_groups(self, student_id: int):
        return self.get_query_set().student_groups(student_id).order_by('-created') 