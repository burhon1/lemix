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

    def teacher_all(self,educenter_id):
        return self.filter(educenter__id__in=educenter_id) \
        .annotate(
            full_name=Concat(F('user__first_name'),Value(' '),F('user__last_name'))
        ).values('id','full_name')

    def teachers_by_course(self,educenter_id,course_id,course_list):
        if course_list is not None:
            from django.contrib.postgres.expressions import ArraySubquery
            return self.filter(group_teacher__course__id=course_id).distinct()\
                        .annotate(
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
                            groups_list=ArraySubquery(course_list)
                        ).values('id','full_name','phone_number','groups_list').order_by('-id')
        
        return self.filter(group_teacher__course__id=course_id)\
                        .annotate(
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
                            groups_list=ArrayAgg(Cast('group_teacher__title', TextField()),distinct=True)
                        ).values('id','full_name','phone_number','groups_list').order_by('-id')

    def main_teacher(self):
        return self.filter(teacer_type=True)

    def teacher_list(self,educenter_id):
        return self.filter(teacer_type=True,educenter__id__in=educenter_id) \
        .annotate(
            full_name=Concat(F('user__first_name'),Value(' '),F('user__last_name'))
        ).values('id','full_name')

    def trainer_list(self):
        return self.filter(teacer_type=False)

class TeacherManager(Manager):
    def get_query_set(self):
        return TeacherQueryset(self.model)

    def teachers(self,educenter_id):
        return self.get_query_set().teachers(educenter_id)  

    def teacher_list(self,educenter_id):
        return self.get_query_set().teacher_list(educenter_id) 

    def teacher_all(self,educenter_id):
        return self.get_query_set().teacher_all(educenter_id)
    
    def teachers_by_course(self,educenter_id,course_id,course_list=None):
        return self.get_query_set().teachers_by_course(educenter_id,course_id,course_list)
    
    def main_teacher(self):
        return self.get_query_set().main_teacher() 

    def trainer_list(self):
        return self.get_query_set().trainer_list()    

    def teacher(self,id):
        return self.get_query_set().teacher(id)  
