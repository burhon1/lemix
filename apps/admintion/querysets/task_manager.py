from django.db.models import Value, Case, When,F,Manager, TextField, CharField,Q
from django.db.models.functions import Cast, Concat, Substr
from django.db.models.query import QuerySet
from django.contrib.postgres.aggregates import ArrayAgg
from django.utils import timezone
class TasksQueryset(QuerySet):
    def get_info(self):
        if not self.exists():
            return self.all()
        return self.values(
            'id', 
            'task_type',
            'deadline',
            'whom',
            'user_status',
            'comment',
            'status'
        )
    def tasks(self):
        return self.get_info()

    def task(self, id):
        return self.get_info().values(
            'groups',
            'leads',
            'students',
            'courses',
            'parents', 
            ).filter(id=id).first()

    def group_tasks(self, id):
        return self.get_info().values(
            'id', 
            'task_type',
            'deadline',
            'comment',
            'status',
            # 'responsibles',
            'created_at'
        ).annotate(
            type = F('task_type__task_type'),
            responsible_staffs = ArrayAgg(Concat(F('responsibles__last_name'), Value(' '), F('responsibles__first_name')), distinct=True),
            today_tasks = ArrayAgg(
                Cast('deadline', TextField()),
                filter=Q(deadline__date=timezone.now().date()
            ))
        ).filter(groups__id__in=[id]).order_by('-deadline')


class TasksManager(Manager):
    def get_query_set(self):
        return TasksQueryset(self.model)
    
    def tasks(self):
        return self.get_query_set().objects()

    def task(self, id):
        return self.get_query_set().task(id)

    def group_tasks(self, id):
        return self.get_query_set().group_tasks(id)