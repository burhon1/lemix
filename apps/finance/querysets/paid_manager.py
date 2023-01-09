from django.db.models import QuerySet, Manager, Sum, F, Q, Count
from django.utils import timezone

class PaidQuerySet(QuerySet):
    def get_info(self):
        return self.all()

    def course_payments(self, course_id: int=None):
        kwargs = dict()
        if course_id:
            kwargs.setdefault('group__course_id', course_id)
        return self.get_info().values(
            'id', 'paid', 'created',
            ).annotate(
                month = F('created__month'),
            ).filter(**kwargs)
    
    def group_payments(self, group_id: int=None):
        curr_year = timezone.now().year
        kwargs = {'created__year': curr_year}
        if group_id:
            kwargs.setdefault('group_id', group_id)
        return self.get_info().values(
            'id', 'paid', 'status'
            ).annotate(
                month = F('created__month'),
            ).filter(**kwargs)
            # .aggregate(
            #     jan = Sum('paid', filter=Q(created__year=curr_year)&Q(created__month=1), default=0),
            #     feb = Sum('paid', filter=Q(created__year=curr_year)&Q(created__month=2), default=0),
            #     mar = Sum('paid', filter=Q(created__year=curr_year)&Q(created__month=3), default=0),
            #     apr = Sum('paid', filter=Q(created__year=curr_year)&Q(created__month=4), default=0),
            #     may = Sum('paid', filter=Q(created__year=curr_year)&Q(created__month=5), default=0),
            #     jun = Sum('paid', filter=Q(created__year=curr_year)&Q(created__month=6), default=0),
            #     jul = Sum('paid', filter=Q(created__year=curr_year)&Q(created__month=7), default=0),
            #     aug = Sum('paid', filter=Q(created__year=curr_year)&Q(created__month=8), default=0),
            #     sep = Sum('paid', filter=Q(created__year=curr_year)&Q(created__month=9), default=0),
            #     oct = Sum('paid', filter=Q(created__year=curr_year)&Q(created__month=10), default=0),
            #     now = Sum('paid', filter=Q(created__year=curr_year)&Q(created__month=11), default=0),
            #     dec = Sum('paid', filter=Q(created__year=curr_year)&Q(created__month=12), default=0),
            # )

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
    def get_queryset(self):
        return PaidQuerySet(self.model)

    def course_payments(self, course_id: int=None):
        return self.get_queryset().course_payments(course_id=course_id)

    def group_payments(self, group_id: int=None):
        return self.get_queryset().group_payments(group_id=group_id)

    def categorical_status(self):
        return self.get_queryset().cat_status()