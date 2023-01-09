from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from finance.chooses import MONTHS
from finance.models import IncomeExpense, Paid
from finance.selectors.reports import get_payment_stats
from admintion.models import Group, Course

@login_required
def financial_reports(request):
    cashflow = IncomeExpense.ie_objects.by_category(1)
    print(cashflow)
    PandL = IncomeExpense.ie_objects.by_category(2)
    print(PandL)
    context = {
        'income': 0, 'debt': 0, 'expense': 0, 'vaucher': 0,
        'income_perc': 0, 'debt_perc': 0, 'expense_perc': 0, 'vaucher_perc': 0,
        'months': dict(MONTHS),
        'soums': [],
        'cashflow': cashflow,
        'PandL': PandL,
        'groups': Group.groups.groups(short_info=True),
        'courses': Course.courses.courses(short_info=True)
    }
    return render(request, 'admintion/moliyaviy_hisobot.html', context)


@login_required
def payments(request):
    """
    Guruh va Kurslar uchun umumiy.
    """

    group_id = request.GET.get('group', None)
    course_id = request.GET.get('course', None)
    if group_id:
        payments = Paid.paid_objects.group_payments(group_id)
    elif course_id:
        payments = Paid.paid_objects.course_payments(course_id)
    else:
        payments = Paid.paid_objects.group_payments()

    context = {
        'income': 0, 'debt': 0,
        'income_perc': 0, 'debt_perc': 0,
        'months': dict(MONTHS),
        'soums': []
    }

    context.update(
        get_payment_stats(payments)
        )
    print(context)
    return JsonResponse(context)