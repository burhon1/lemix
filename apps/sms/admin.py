from django.contrib import admin
from .models import SMSAccount, SMSMessage

admin.site.register(SMSAccount)
admin.site.register(SMSMessage)
