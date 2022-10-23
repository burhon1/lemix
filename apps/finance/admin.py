from django.contrib import admin

from finance.models import Paid,StudentBalance

# Register your models here.
admin.site.register(Paid)
admin.site.register(StudentBalance)