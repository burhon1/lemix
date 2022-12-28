from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from finance.chooses import MONTHS
from finance.selectors.reports import get_by_category
from admintion.models import Group, Course

@login_required
def financial_reports(request):
    cashflow = get_by_category(1)
    print(cashflow)
    PandL = get_by_category(2)
    context = {
        'income': 0, 'debt': 0, 'expense': 0, 'vaucher': 0,
        'income_perc': 0, 'debt_perc': 0,
        'months': dict(MONTHS),
        'soums': [],
        'cashflow': cashflow,
        'PandL': PandL
    }
    return render(request, 'admintion/moliyaviy_hisobot.html', context)


@login_required
def payments(request):
    """
    Guruh va Kurslar uchun umumiy.
    """
    group_id = request.GET.get('group', None)
    if group_id:
        group = get_object_or_404(Group, pk=int(group_id))
    else:
        course_id = request.GET.get('course', None)
        if course_id:
            course = get_object_or_404(Course, pk=int(course_id))

    context = {
        'income': 0, 'debt': 0,
        'income_perc': 0, 'debt_perc': 0,
        'months': dict(MONTHS),
        'soums': []
    }

    return JsonResponse(context)