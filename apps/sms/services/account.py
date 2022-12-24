from django.shortcuts import redirect, render,reverse
from django.conf import settings
import requests, json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from sms.utils import get_new_dispatch_id
from sms.models import SMSMessage, SMSAccount

url = "http://notify.eskiz.uz/api"

def get_account():
    return SMSAccount.objects.first()


def get_token(email,password):
    endpoint=f"{url}/auth/login"
    data2 = {
        "email":email,
        "password":password
    }
    vash_token_zdes=requests.post(endpoint, data=data2).json()['data']['token']
    return vash_token_zdes

def send_message(phone_number,text,request, email=None,password=None):

    if (email and password) is None:
        account = get_account()
        if account:
            return 404
        email, password = account.credentials
    token = get_token(email,password)

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "mobile_phone": f"998{phone_number}",
        "message":text, 
        "from":"4546",
        "callback_url": request.build_absolute_uri(reverse('sms:get-callback')) if request else "http://0000.uz/test.php"
    }
    try:
        res = requests.post(f"{url}/message/sms/send",data=data, headers=headers).json()
        SMSMessage.objects.create(phone_number=f"998{phone_number}")
        return 201
    except:
        return 503

def get_user_info(email, password):

    endpoint = f"{url}/auth/user"
    headers = {
        'Authorization': f'Bearer {get_token(email, password)}'
    }

    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_user_balance(email, password):
    response = get_user_info(email,password)
    try:
        return response['balance']
    except KeyError:
        return 

def need_items(data, fields=None):
    items = []
    for dt in data:
        dt2 = []
        for key,value in dt.items():
            if key in fields:
                if key in ['created_at', 'updated_at']:
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(ZoneInfo(settings.TIME_ZONE)).strftime('%Y-%m-%d %H:%M:%S')
                dt2.append((key,value))
        items.append(dict(dt2))
    return items


def get_messages_by_dispatch(email=None, password=None, dispatch_id=None, page=None, sms_message:SMSMessage=None):
    """
    Service function returns as `messages`, `pages` grouped per-20 or [], [] if not response from SMS Provider.
    """

    if (email and password) is None:
        account = get_account()
        if account:
            return 404
        email, password = account.credentials

    token = get_token(email, password)

    endpoint = f"{url}/message/sms/get-user-messages-by-dispatch"
    payload = {
        'dispatch_id': dispatch_id
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }

    res = requests.post(endpoint, data=payload, headers=headers)
    if res.status_code == 200:
        res = res.json()
        messages = res['data']['data']
        pages = [page['label'] for page in res['data']['links'] if page['label'] not in ["&laquo; Previous", "Next &raquo;"]  ]
        price = 0
        created_at = updated_at = datetime.now()
        for p in pages:
            res = requests.post(endpoint+f'?page={p}', data=payload, headers=headers)
            res = res.json()
            
            if page and p == page:
                messages = res['data']['data']
            price+=sum([ m['price'] for m in res['data']['data'] if type(m['price'])==int])
        if len(messages) > 0:
            created_at = datetime.strptime(messages[0]['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(ZoneInfo(settings.TIME_ZONE))
            updated_at = datetime.strptime(messages[-1]['updated_at'], '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(ZoneInfo(settings.TIME_ZONE))
        timedelta = updated_at - created_at

        if not sms_message:
            sms_message = SMSMessage.objects.get(dispatch_id=dispatch_id)
        diff = sms_message.set_price(price)
        

        if diff > 0:
            sms_account = SMSAccount.objects.first()
            if sms_account:
                sms_account.set_sent_sms(sms_count=0, sms_soums=price)
        sms_message.update({'sms_count': res['data']['total'], 'timedelta': timedelta.total_seconds()})
        messages = need_items(messages, fields=('to', 'status', 'status_date', 'country_code', 'price', 'updated_at'))
        return messages, pages

    return [], []


def send_messages(email, password, text, request, phone_numbers=[], users=[]):
    dispatch_id = get_new_dispatch_id()

    if (email and password) is None:
        account = get_account()
        if account is None:
            return 404
        email, password = account.credentials
    token = get_token(email, password)

    endpoint = f"{url}/message/sms/send-batch"
    
    messages = []
    for phone in phone_numbers:
        messages.append({
            'user_sms_id': '452', 'to': int(f'998{phone}'), 'text': text
        })
    for user in users:
        messages.append({
            "user_sms_id":"452","to": int(f"998{user.phone}"), "text": text
        })
    json_data = {
        'dispatch_id':dispatch_id,
        'from':"4546",
        'messages': messages
    }

    headers = {
        "Authorization":f"Bearer {get_token(email, password)}"
    }
    try:
        res = requests.post(endpoint, json=json_data, headers=headers).json()
        SMSMessage.objects.create(dispatch_id=dispatch_id, message=text, who_sent=request.user, type="Xabar")
        account = get_account()
        if account:
            account.set_sent_sms(sms_count=len(messages), sms_soums=0)
        return 200
    except:
        return 503
