from typing import List
from django.db.models import Value, F,Manager
from django.db.models.functions import Concat
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet

from admintion.models import Course


class ContentsQueryset(QuerySet):
    def get_info(self):
        if not self.exists():
            return self.all()
        return self.values(
            'id',
            'title', 'order', 
            'opened_at', 'closed_at'
        )

    def contents(self):
        return self.get_info()

    def content(self, id: int):
        return self.get_info().values(
            'id',
            'title', 'order', 
            'lesson_id', 'lesson__title',
            'content_type', 'video', 'video_link', 'text',
            'students', 'opened_at', 'closed_at'
        ).filter(id=id).first()

    def homeworks(self, courses:List[int]):
        return self.get_info().values(
            'id', 
            'title', 
            'order',
            'opened_at', 'closed_at',
            ).filter(lesson__module__course_id__in=courses)

class ContentsManager(Manager):
    def get_query_set(self):
        return ContentsQueryset(self.model)

    def contents(self):
        return self.get_query_set().contents()

    def content(self, id: int):
        return self.get_query_set().content(id)

    def homeworks(self, courses: List[int]):
        return self.get_query_set().homeworks(courses)