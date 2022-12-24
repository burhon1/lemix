from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from sms.models import SMSAccount

def account_view(request):

    return JsonResponse(dict())

