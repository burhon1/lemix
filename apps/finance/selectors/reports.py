from typing import List, Dict
from django.db.models import QuerySet
from django.utils import timezone


def get_payment_stats(payments:QuerySet):
    incomes: List[int] = []
    debts: List[int] = []
    curr_month = timezone.now().month
    income_perc, debt_perc = 0, 0
    income1, debt1 = 0, 0

    for month in range(1, 13):
        income = sum([payment['paid'] for payment in payments.filter(status=True, month=month)]) or 0  
        incomes.append(income)
        
        debt = sum([payment['paid'] for payment in payments.filter(status=False, month=month)]) or 0  
        debts.append(debt)
        if month == curr_month:
            income1, debt = income, debt
            try:
                income_perc = income / incomes[-1]
                income_perc = (income_perc - 1) * 100

            except:
                income_perc = 100
            
            try:
                debt_perc = debt / debts[-1]
                debt_perc = (1 - debt_perc) * 100
            except:
                debt_perc = 100
    return {
        'incomes': incomes, 'debts': debts, 'income_perc': income_perc, 'debt_perc': debt_perc,
        'income': income1, 'debt': debt1, 
    }