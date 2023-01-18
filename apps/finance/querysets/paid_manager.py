from django.db.models import QuerySet, Manager, Sum, F, Q, Count

class PaidQuerySet(QuerySet):
    def get_info(self):
        return self.all()

    def course_payments(self, course_id: int=None):
        kwargs = dict()
        if course_id:
            kwargs.setdefault('group__course_id', course_id)
        return self.get_info().values(
            'id', 'paid', 'created'
            ).filter(**kwargs)
    
    def group_payments(self, group_id: int=None):
        kwargs = dict()
        if group_id:
            kwargs.setdefault('group_id', group_id)
        self.get_info().values(
            'id', 'paid', 'created'
            ).filter(**kwargs)

    def cat_status(self):
        """
        Categorical status
        """
        return self.model.objects.aggregate(
            cash = Count('paid_type', filter=Q(paid_type=1)),
            terminal = Count('paid_type', filter=Q(paid_type=2)),
            plastic = Count('paid_type', filter=Q(paid_type=3)),
            via_bank = Count('paid_type', filter=Q(paid_type=4)),
            click = Count('paid_type', filter=Q(paid_type=5)),
            payme = Count('paid_type', filter=Q(paid_type=6)),
            apelsin = Count('paid_type', filter=Q(paid_type=7)),
            stripe = Count('paid_type', filter=Q(paid_type=8)),
        )

class PaidManager(Manager):
    """
        Bu class paid modeli uchun yozilgan manager
        :func obj | None course_payments: bu funksiyani 
            chaqirganda unga course_id parameter keladi 
            uning turi int. Bu funksiya qaytarishdan oldin 
            get_queryset funksiyasini chaqiradi va uning 
            course_payments funksiyasiga murojat qiladi.
            murojat qilingan funksiyaning course_id parameterga 
            course_payments dan kelgan course_id beriliadi bu bizga 
            course id si shunga tenglarini qaytaradi
    """
    def get_queryset(self):
        return PaidQuerySet(self.model)

    def course_payments(self, course_id: int):
        return self.get_queryset().course_payments(course_id=course_id)

    def group_payments(self, group_id: int):
        return self.get_queryset().group_payments(group_id=group_id)

    def categorical_status(self):
        return self.get_queryset().cat_status()