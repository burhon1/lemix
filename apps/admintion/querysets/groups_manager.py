from django.db.models import Value, Case, When,F,Manager,Func,IntegerField,Subquery,CharField,TextField,Sum,OuterRef,Count
from django.contrib.postgres.aggregates import ArrayAgg
# from django.contrib.postgres.functions import ToArray
from django.db.models.functions import Concat,Substr,Cast
from django.db.models.query import QuerySet

# from admintion.models import Student

class GroupQueryset(QuerySet):
    def get_info(self,educenter_id,short_info=False):
        datas = None
        if  not self.exists():
            datas = self.all()
        elif short_info:
            return self.get_info(educenter_id).values('id', 'title')    
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
                'start_date'
            ).annotate(
                course=F("course__title"),
                teacher=Concat(F('teacher__user__first_name'),Value(' '),F('teacher__user__last_name')),
                times = Concat(Substr(Cast(F('start_time'), TextField()),1,5),Value('-'),Substr(Cast(F('end_time'), TextField()),1,5),output_field=CharField()),
                total_student=Count('students',distinct=True),
                days = ArrayAgg(Cast('days__days', TextField()),distinct=True),
                formatted_date=Func(
                    F('start_date'),
                    Value('DD-MM-YYYY'),
                    function='to_char',
                    output_field=CharField()
                )
                )
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
                'formatted_date'
            )
        return self.get_info(educenter_ids).values(
                *columns
            ).order_by('-id')  
    def group_list(self,educenter_id):
        return self.get_info(educenter_id,True)        

    def group(self,id,educenter_ids):
        return self.get_info(educenter_ids).values(
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

    def group_filter(self,filters,educenter_ids):
        return self.filter(educenter__id__in=educenter_ids) \
        .filter(**filters) \
        .values(
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
            )\
        .annotate(
            course=F("course__title"),
            teacher=Concat(F('teacher__user__first_name'),Value(' '),F('teacher__user__last_name')),
            times = Concat(Substr(Cast(F('start_time'), TextField()),1,5),Value('-'),Substr(Cast(F('end_time'), TextField()),1,5),output_field=CharField()),
            total_student=Count('students',distinct=True),
            days = ArrayAgg(Cast('days__days', TextField()),distinct=True),
        )

    def group_content(self,educenter_id):
        return self.filter(educenter__id__in=educenter_id)\
                    .annotate(
                        course_title=F("course__title"),
                        teacher_fio=Concat(F('teacher__user__first_name'),Value(' '),F('teacher__user__last_name')),
                        video_count=Sum(Case(
                            # This could depend on the related name for the paragraph -> document relationship
                            When(modules__lessons__contents__content_type=1, then=Value(1)),
                            default=Value(0),
                            output_field=IntegerField(),
                        )),
                        text_count=Sum(Case(
                            # This could depend on the related name for the paragraph -> document relationship
                            When(modules__lessons__contents__content_type=2, then=Value(1)),
                            default=Value(0),
                            output_field=IntegerField(),
                        )),
                        test_count=Sum(Case(
                            # This could depend on the related name for the paragraph -> document relationship
                            When(modules__lessons__contents__content_type=3, then=Value(1)),
                            default=Value(0),
                            output_field=IntegerField(),
                        )),
                        homework_count=Sum(Case(
                            # This could depend on the related name for the paragraph -> document relationship
                            When(modules__lessons__contents__content_type=4, then=Value(1)),
                            default=Value(0),
                            output_field=IntegerField(),
                        )),
                        content_count=Count('modules__lessons__contents', distinct=True),
                    ).values('id','title','course_title','teacher_fio','video_count','text_count','test_count','homework_count','content_count','course__id').order_by('-id')

    def groups_by_course(self,course_id,educenter_ids,short_info):
        return self.filter(course__id=course_id).groups(educenter_ids,short_info=short_info)

    def group_filter_list(self,filters,educenter_ids):
        return self.filter(educenter__id__in=educenter_ids) \
                    .filter(**filters).values('id','title')

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
    
    def groups_by_course(self,educenter_ids, course_id, short_info=False):
        return self.get_query_set().groups_by_course(course_id,educenter_ids,short_info) 

    def group_list(self,educenter_id):
        return self.get_query_set().group_list(educenter_id)   
    
    def group_content(self,educenter_id):
        return self.get_query_set().group_content(educenter_id)

    def group_filter(self,filters,educenter_ids):
        return self.get_query_set().group_filter(filters,educenter_ids) 

    def group_filter_list(self,filters,educenter_ids):
        return self.get_query_set().group_filter_list(filters,educenter_ids)

    def group(self,id,educenter_ids):
        return self.get_query_set().group(id,educenter_ids)  

