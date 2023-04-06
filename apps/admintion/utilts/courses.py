from django.db.models import Q


def course_count_condition(type,group=False):
    if group:
        return Q(Q(modules__lessons__contents__content_type=type)&Q(modules__lessons__contents__groups__isnull=True))|Q(Q(modules__lessons__contents__groups__id=group)&Q(modules__lessons__contents__content_type=type))
    return Q(modules__lessons__contents__content_type=type)&Q(modules__lessons__contents__groups__isnull=True)
