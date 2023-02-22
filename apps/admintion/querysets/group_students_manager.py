from django.db.models import Value, Case, When,F,Manager, TextField, CharField,Q,Count,Sum,IntegerField
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

    def pay_by_lesson(self):
        return self.filter(Q(student__pay_type=1) | Q(group__pay_type=1)).\
            annotate(group_days=ArrayAgg('group__days__days',distinct=True)).\
            values('group__title','student__id','created','group__start_date','group_days','group__course__price')

    def pay_by_month(self):
        return self.filter(Q(student__pay_type=2) | Q(group__pay_type=2)).\
            annotate(group_days=ArrayAgg('group__days__days',distinct=True)).\
            values(
            'group__title',
            'student__id',
            'created',
            'group__start_date',
            'group_days',
            'group__course__price') 

    def pay_by_year(self):
        return self.filter(Q(student__pay_type=3) | Q(group__pay_type=3)).\
            annotate(group_days=ArrayAgg('group__days__days',distinct=True)).\
            values(
                'group__title',
                'student__id',
                'created',
                'group__start_date',
                'group_days',
                'group__course__price')

    def pay_by_module(self):
        return self.filter(Q(student__pay_type=4) | Q(group__pay_type=4)).\
            annotate(group_days=ArrayAgg('group__days__days',distinct=True)).\
            values('group__title','student__id','created','group__start_date','group_days','group__course__price')

    def student_add_group(self,user):
        return self.filter(student__user=user).values_list('id',flat=True)

    def student_filter(self,filters,educenter_ids):
        from admintion.models import GroupStudents
        # print()
        return self.filter(group__educenter__id__in=educenter_ids).filter(**filters).annotate(
            student_ids=F('student__id'),
            fio=Concat(
                F('student__user__first_name'),
                Value(' '),
                F('student__user__last_name'),
                Value(' '),
                F('student__user__middle_name')
                ),
            phone=Concat(
                Value('+998'),
                Value(' ('),
                Substr(F('student__user__phone'),1,2),
                Value(') '),
                Substr(F('student__user__phone'),3,3),
                Value(' '),
                Substr(F('student__user__phone'),6,2),
                Value(' '),
                Substr(F('student__user__phone'),8,2)
                ),
            student_status=Case(
                When(student__status=1,then=Value('Aktiv')),
                When(student__status=2,then=Value('Muzlatilgan')),
                When(student__status=3,then=Value('Ketgan')),
                output_field=CharField()
            ),
            group_count = Count(F('student__ggroups'), distinct=True),
            payment = Sum(F('student__payment__paid'), distinct=True),
            attendace = ArrayAgg(F('student__ggroups__attendance'), distinct=True)
        ).values('id','student_ids','fio','phone','student_status','group_count','payment','attendace')    

    def student_list(self,filters,educenter_ids):
        return self.filter(group__educenter__id__in=educenter_ids)\
            .filter(**filters)\
            .annotate(
                student_ids=F('student__id'),
                fio=Concat(
                    F('student__user__first_name'),
                    Value(' '),
                    F('student__user__last_name'),
                    Value(' '),
                    F('student__user__middle_name')
                    )
            )
class GroupStudentManager(Manager):
    def get_query_set(self):
        return GroupStudentsQueryset(self.model)
    
    def objects(self):
        return self.get_query_set().objects().order_by('-created')

    def student_add_group(self,user):
        return self.get_query_set().student_add_group(user)   

    def student_groups(self, student_id: int):
        return self.get_query_set().student_groups(student_id).order_by('-created')

    def student_filter(self,filters,educenter_ids):
        return self.get_query_set().student_filter(filters,educenter_ids)     

    def student_list(self,filters,educenter_ids):
        return self.get_query_set().student_list(filters,educenter_ids)

    def pay_by_lesson(self):
        return self.get_query_set().pay_by_lesson() 
    def pay_by_month(self):
        return self.get_query_set().pay_by_month() 
    def pay_by_year(self):
        return self.get_query_set().pay_by_year() 
    def pay_by_module(self):
        return self.get_query_set().pay_by_module()                            