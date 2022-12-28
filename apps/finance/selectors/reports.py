from finance.models import IncomeExpense


def get_income(**filter_kwargs):
    return IncomeExpense.ie_objects.by_type(1, *filter_kwargs)

def get_expense(**filter_kwargs):
    return IncomeExpense.ie_objects.by_type(2, *filter_kwargs)

def get_by_category(category: int, **kwargs):
    incomes = IncomeExpense.ie_objects.by_category(category, **kwargs).prefetch_related('fields')

    return incomes