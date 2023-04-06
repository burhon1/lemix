from django.db.models import Value,CharField, Count, When,F,Manager,Func,IntegerField,Q,TextField,Exists,OuterRef, Sum
from django.db.models.functions import Concat,Substr,Cast
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet

class StudentQueryset(QuerySet):
    def get_info(self,educenter_ids=None):
        if not self.exists():
            return self.all()
        return self.filter(educenter__id__in=educenter_ids).values(
            'id',
            'user__first_name',
            'user__last_name',
        ).annotate(
            full_name=Concat(F('user__first_name'),Value(' '),F('user__last_name'))
        )

    def students(self,educenter_ids):
        return self.get_info(educenter_ids).values(
            'id',
            'user__first_name',
            'user__last_name',
            'user__phone',
            # 'groups',
            'status'
        ).annotate(
            full_name = Concat(F('user__last_name'),Value(' '),F('user__first_name')),
            phone_number = Concat(
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
            group_count = Count(F('ggroups'), distinct=True),
            payment = Sum(F('payment__paid'), distinct=True),
            attendace = ArrayAgg(F('ggroups__attendance'), distinct=True)
        ).order_by('-id')

    def students_attendace(self,id,educenter_ids):
        return self.get_info(educenter_ids).filter(ggroups__group__id=id).values(
            'id',
            'full_name'
        ).annotate(
            attendace_status=ArrayAgg(
                Cast('ggroups__attendance__status', TextField()),
                filter=Q(ggroups__attendance__status__isnull=False
            ))
        ).annotate(
            attendace=ArrayAgg(
                Cast('ggroups__attendance__date', TextField()),
                filter=Q(ggroups__attendance__date__isnull=False
            )),
            comment=ArrayAgg(
                Cast('ggroups__attendance__comment', TextField()),
                filter=Q(ggroups__attendance__comment__isnull=False
            )),
            reasen=ArrayAgg(
                Cast('ggroups__attendance__reasen', TextField()),
                filter=Q(ggroups__attendance__comment__isnull=False
            ))
        )

    def student_balances(self,id,educenter_ids):
        return self.get_info(educenter_ids).filter(ggroups__id=id).values(
            'id',
            'full_name',
            'payment__paid',
            'payment__created',
            ).annotate(
                attendaces=ArrayAgg(Cast('ggroups__attendance__date', TextField()),distinct=True)
            )

    def students_by_status(self, status: int=1):
        return self.get_info().filter(status=status)
    
    def student_detail(self, id: int):
        return self.get_info().values(
            'id',
            'groups',
            'status',
            # 'source',
            'comment',
            'user__first_name', 'user__last_name', 'user__middle_name',
            'balance'
        ).annotate(
            full_name = Concat(F('user__last_name'),Value(' '),F('user__first_name')),
            phone_number = Concat(
                Value('+998'), F('user__phone')),
            gender = F('user__gender'),
            birthday = F('user__birthday'),
            location = F('user__location'),
            payment = Sum(F('payment__paid'), distinct=True),
            picture = F('user__picture'),
            source = F('source__title'),

        ).filter(id=id).first()

    def student_short_detail(self, id: int):
        return self.get_info().values(
            'id',
            'ggroups',
            'status',
        ).annotate(
            full_name = Concat(F('user__last_name'),Value(' '),F('user__first_name')),
            phone_number = Concat(
                Value('+998'), F('user__phone')),
            sgroups = ArrayAgg(F('ggroups__group__title')),
        ).filter(id=id).first()

    def students_by_course(self,educenter_ids,pk):
        return self.filter(ggroups__group__course__id=pk)\
                    .annotate(
                        full_name = Concat(F('user__last_name'),Value(' '),F('user__first_name')),
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
                        group_count=Count(F('ggroups__group__id'),distinct=True)
                    ).values('id','full_name','phone_number','group_count','status')

    def student_list(self,educenter_ids,group_id):
        return self.get_info(educenter_ids).filter(status=1).exclude(ggroups__group__id=group_id).values('id','full_name') 

    def students_by_status(self):
        # from admintion.data import chooses
        # content = {}
        # for status in chooses.STUDENT_STATUS:
        #     print(status[1])
        # print(chooses.STUDENT_STATUS)
        return {
            'active_students':self.filter(status=1).count(),
            'nonactive_students':self.filter(status=2).count(),
            'removed_students':self.filter(status=3).count()
        }
    def student_filter(self,filters,educenter_ids):
        return self.filter(educenter__id__in=educenter_ids).filter(**filters)    

    def studet_short_list(self,filters,educenter_ids):
        return self.filter(educenter__id__in=educenter_ids)\
            .filter(**filters)\
            .annotate(
                full_name = Concat(F('user__last_name'),Value(' '),F('user__first_name'))
            )\
            .values('id','full_name')

class StudentManager(Manager):
    def get_query_set(self):
        return StudentQueryset(self.model)
    
    def students(self,educenter_ids):
        return self.get_query_set().students(educenter_ids) 
    
    def students_by_course(self,educenter_ids,pk):
        return self.get_query_set().students_by_course(educenter_ids,pk)

    def students_attendace(self,id,educenter_ids):
        return self.get_query_set().students_attendace(id,educenter_ids)
        
    def student_balances(self,id,educenter_ids):
        return self.get_query_set().student_balances(id,educenter_ids)

    def student_detail(self, id):
        return self.get_query_set().student_detail(id)

    def studet_list(self,educenter_ids,group_id=None):
        return self.get_query_set().student_list(educenter_ids,group_id)

    def studet_short_list(self):
        return self.get_query_set().studet_short_list()    

    def student_filter(self,filters,educenter_ids):
        return self.get_query_set().student_filter(filters,educenter_ids)

    def students_by_status(self):
        return self.get_query_set().students_by_status()

  
