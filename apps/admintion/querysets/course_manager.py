from django.db.models import Value, Count,Case, When,F,Manager, Q,TextField,BigAutoField, CharField,IntegerField,Sum
from django.db.models.functions import Cast, Concat, Substr
from django.db.models.query import QuerySet
from django.contrib.postgres.aggregates import ArrayAgg

from admintion.utilts.courses import course_count_condition

class CoursesQueryset(QuerySet):
    def get_info(self,educenter_id):
        return self.filter(educenter__id__in=educenter_id)

    def courses(self, educenter_id,short_info=False):
        if short_info:
            return self.get_info(educenter_id).values('id', 'title')
        return self.get_info(educenter_id)\
            .annotate(
                group_count=Count(F('group'), distinct=True),
                student_count=Count(F('group__students'), distinct=True)
            )\
            .order_by('-id')   

    def course_filter(self,filters,educenter_ids):
        return self.filter(educenter__id__in=educenter_ids) \
        .filter(**filters) \
        .annotate(
            group_count=Count(F('group'), distinct=True),
            student_count=Count(F('group__students'), distinct=True)
        )\
        .values(
            'id',
            'title',
            'duration',
            'price',
            'group_count',
            'student_count',
            'status'
        )\
        .order_by('-id')

    def course(self, id):
        return self.filter(id=id)\
                    .annotate(
                        group_count=Count('group', distinct=True),
                        student_count=Count('group__students', distinct=True),
                        course_duration=Case(
                                    When(duration_type=1,then=Concat(F('duration'),Value(' '),Value('kun'))), 
                                    When(duration_type=2,then=Concat(F('duration'),Value(' '),Value('oy'))), 
                                    default= Concat(F('duration'),Value(' '),Value('yil')),
                                    output_field=CharField()
                        ),
                        course_lesson_duration=Case(
                                    When(lesson_duration_type=1,then=Concat(F('lesson_duration'),Value(' '),Value('daqiqa'))), 
                                    default= Concat(F('lesson_duration'),Value(' '),Value('soat')),
                                    output_field=CharField()
                        ),
                        course_price=Case(
                                    When(price_type=1,then=Concat(F('price'),Value(' '),Value('so\'m'))), 
                                    When(price_type=2,then=Concat(F('price'),Value(' '),Value('rubl'))), 
                                    default= Concat(F('duration'),Value(' '),Value('dollar')),
                                    output_field=CharField()
                        ),
                        teacher_count=Case(
                                    When(group__teacher__isnull=False,group__trainer__isnull=True,then=Concat(Value(1),Value('ta(0)'))),
                                    When(group__teacher__isnull=False,group__trainer__isnull=False,then=Concat(Value(1),Value('ta(1)'))),
                                    default=Value('0ta(0)'),
                                    output_field=CharField()
                        )
                    ).values('id','title','course_duration','course_lesson_duration','course_price','group_count','teacher_count','student_count','duration','duration_type','lesson_duration','lesson_duration_type','price','price_type','comment').first()

    def course_contents(self,educenter_id,user):
        data = self.filter(educenter__id__in=educenter_id)
        if user is not None:
            data = data.filter(group__teacher__user=user)
        return data\
                    .annotate(
                        student_count=Count('modules__lessons__contents', distinct=True),
                        group_count=Count('group', distinct=True),
                        video_count=Count(Case(
                            # This could depend on the related name for the paragraph -> document relationship
                            When(course_count_condition(1), then=Value(1)),
                            output_field=IntegerField(),
                        ),distinct=True),
                        text_count=Count(Case(
                            # This could depend on the related name for the paragraph -> document relationship
                            When(course_count_condition(2), then=F('modules__lessons__contents__id')),
                            output_field=IntegerField()
                        ),distinct=True),
                        test_count=Count(Case(
                            # This could depend on the related name for the paragraph -> document relationship
                            When(course_count_condition(3), then=F('modules__lessons__contents__id')),
                            output_field=BigAutoField(),
                        ),distinct=True),
                        homework_count=Count(Case(
                            # This could depend on the related name for the paragraph -> document relationship
                            When(course_count_condition(4), then=F('modules__lessons__contents__id')),
                            output_field=IntegerField(),
                        ),distinct=True),
                        content_count=Count(Case(
                            # This could depend on the related name for the paragraph -> document relationship
                            When(modules__lessons__contents__groups__isnull=True, then=F('modules__lessons__contents__id')),
                            output_field=BigAutoField(),
                        ),distinct=True)
                    ).values('id','title','group_count','video_count','text_count','test_count','homework_count','content_count').order_by('-id')

    def course_content(self,course_id,group):
        return self.filter(id=course_id).annotate(
                        student_count=Count('modules__lessons__contents', distinct=True),
                        group_count=Count('group', distinct=True),
                        video_count=Count(Case(
                            # This could depend on the related name for the paragraph -> document relationship
                            When(course_count_condition(1,group), then=F('modules__lessons__contents__id')),
                            output_field=IntegerField(),
                        ),distinct=True),
                        text_count=Count(Case(
                            # This could depend on the related name for the paragraph -> document relationship
                            When(course_count_condition(2,group), then=F('modules__lessons__contents__id')),
                            output_field=IntegerField(),
                        ),distinct=True),
                        test_count=Count(Case(
                            # This could depend on the related name for the paragraph -> document relationship
                            When(course_count_condition(3,group), then=F('modules__lessons__contents__id')),
                            output_field=IntegerField(),
                        ),distinct=True),
                        homework_count=Count(Case(
                            # This could depend on the related name for the paragraph -> document relationship
                            When(course_count_condition(4,group), then=F('modules__lessons__contents__id')),
                            output_field=IntegerField(),
                        ),distinct=True),
                        content_count=Count(Case(
                            # This could depend on the related name for the paragraph -> document relationship
                            When(Q(modules__lessons__contents__groups__isnull=True)|Q(modules__lessons__contents__groups__id=group), then=F('modules__lessons__contents__id')),
                            output_field=BigAutoField(),
                        ),distinct=True),
                    ).values('id','title','group_count','video_count','text_count','test_count','homework_count','content_count','status').first()

class CoursesManager(Manager):
    def get_query_set(self):
        return CoursesQueryset(self.model)
    
    def courses(self,educenter_id, short_info=False):
        return self.get_query_set().courses(educenter_id,short_info=short_info)

    def course_filter(self,filters,educenter_ids):
        return self.get_query_set().course_filter(filters,educenter_ids)  
    
    def course_contents(self,educenter_id,user=None):
        return self.get_query_set().course_contents(educenter_id,user)
    
    def course_content(self,course_id,group=None):
        return self.get_query_set().course_content(course_id,group)

    def course(self, id):
        return self.get_query_set().course(id)