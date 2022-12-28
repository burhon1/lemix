from email.policy import default
from django.db import models
from finance.chooses import *
from finance.querysets import income_expense_manager, field_manager, record_manager
# Create your models here.
class Paid(models.Model):
    student = models.ForeignKey('admintion.Student',models.CASCADE)
    group = models.ForeignKey('admintion.Group',models.CASCADE,null=True,blank=True)
    paid = models.PositiveBigIntegerField()
    goal_type = models.PositiveSmallIntegerField(choices=GOAL_TYPE)
    paid_type = models.PositiveSmallIntegerField(choices=PAID_TYPE)
    description = models.TextField()
    user = models.ForeignKey('user.CustomUser',models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

class StudentBalance(models.Model):
    title = models.CharField(max_length=100)
    student = models.ForeignKey('admintion.Student',models.CASCADE)
    balance = models.BigIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Talabaning balansi" 
        verbose_name_plural = "Talabaning balanslari"

# demo click
class ClickOrder(models.Model):
    is_paid = models.BooleanField(default=False)
    amount = models.DecimalField(decimal_places=2, max_digits=12)


class IncomeExpense(models.Model):
    title = models.CharField(max_length=120)
    type = models.PositiveSmallIntegerField(choices=INCOME_EXPENSE_TYPE)
    category = models.PositiveSmallIntegerField(choices=INCOME_EXPENSE_CATEGORY, default=1)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('user.CustomUser', models.SET_NULL, null=True)
    objects = models.Manager()
    ie_objects = income_expense_manager.IncomeExpenseManager()
    class Meta:
        verbose_name = 'Income Or Expense'
        verbose_name_plural = 'Income Or Expense'

    def __str__(self):
        return "%s - %s" % (self.title, dict(INCOME_EXPENSE_TYPE)[self.type])


# class IECategory(models.Model):
#     title = models.CharField(max_length=120)
#     type = models.PositiveSmallIntegerField(choices=INCOME_EXPENSE_TYPE)
#     created = models.DateTimeField(auto_now_add=True)
#     author = models.ForeignKey('user.CustomUser', models.SET_NULL, null=True)

#     class Meta:
#         verbose_name = 'Income Or Expense Category'
#         verbose_name_plural = 'Income Or Expense Category'

#     def __str__(self):
#         return self.title


class IEField(models.Model):
    title = models.CharField(max_length=120)
    type = models.ForeignKey(IncomeExpense, models.CASCADE, related_name='fields')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('user.CustomUser', models.SET_NULL, null=True)
    objects = models.Manager()
    fields = field_manager.FieldManager()
    def __str__(self):
        return self.title


class IERecord(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveSmallIntegerField(choices=MONTHS)
    value = models.PositiveIntegerField(null=True)
    field = models.ForeignKey(IEField, models.CASCADE, related_name='records')
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('user.CustomUser', models.SET_NULL, null=True)
    objects = models.Manager()
    records = record_manager.RecordManager()
    def __str__(self):
        return "%s/%s: %s" % (self.year, dict(MONTHS)[self.month], self.field.title)