from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.conf import settings
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from sms.services import get_account, get_user_info, get_user_balance, get_messages_by_dispatch
from sms.models import SMSAccount, SMSMessage 



@csrf_exempt
def get_callback_view(request):
    phone_number = request.POST.get('phone_number')
    status_date = datetime.strptime(request.POST.get('status_date'), "%Y-%m-%d %H:%M:%S").astimezone(ZoneInfo(settings.TIME_ZONE))
    sms = SMSMessage.objects.filter(phone_number=phone_number, status__isnull=True).last()
    sms.country = request.POST.get('country')
    sms.sms_count = request.POST.get('sms_count')
    sms.soums = int(sms.sms_count) * 50
    sms.status = request.POST.get('status')
    sms.timedelta = abs(sms.created_at - status_date).total_seconds()
    sms.save()
    account = get_account()
    account.set_sent_sms(int(sms.sms_count), int(sms.soums))
    return JsonResponse({})


@login_required
def sms_journal_view(request):
    context = dict()
    account = get_account()
    if account:
        balance = get_user_balance(account.email, account.password)
        context.setdefault('balance', balance)
        context.setdefault('sent_sms', account.sent_sms)
        context.setdefault('free_sms', account.free_sms)
        context.setdefault('sent_sms_soums', account.sent_sms_soums)
    context.setdefault('messages', SMSMessage.messages.messages())
    return render(request, 'admintion/sms_jurnali.html', context)


def sms_message_users(request, pk: int):
    
    message = get_object_or_404(SMSMessage, pk=pk)
    if message.phone_number:
        messages = [
            model_to_dict(message, fields=('id', 'phone_number', 'country', 'status', 'soums', 'created_at'))
        ]
        messages[0]['created_at'] = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        pages = []
    else:
        page = request.GET.get('page', None)
        account = get_account()
        if account:
            email, password = account.credentials
            messages, pages = get_messages_by_dispatch(email, password, dispatch_id=message.dispatch_id, page=page, sms_message=message)
        else:
            messages, pages = get_messages_by_dispatch(dispatch_id=message.dispatch_id, page=page, sms_message=message)

    data = {
        'messages':messages, 
        'pages': pages, 
        'count': message.sms_count or 0, 
        'soums': message.soums or 0,
        'timedelta': str(timedelta(seconds=(message.timedelta or 0)))
        }
    return JsonResponse(data)

def send_sms_to_user(request):
    return JsonResponse({'status': 'waiting'})
