from django.contrib import admin

from finance.models import Paid,StudentBalance,ClickOrder,IncomeExpense, IEField, IERecord

# Register your models here.
admin.site.register(Paid)
admin.site.register(StudentBalance)
admin.site.register(IncomeExpense)
admin.site.register(IEField)
admin.site.register(IERecord)