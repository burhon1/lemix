from django.shortcuts import redirect, render, reverse
import requests
from sms.models import SMSMessage

url = "http://notify.eskiz.uz/api"

def get_token(email,password):
    endpoint=f"{url}/auth/login"
    data2 = {
        "email":email,
        "password":password
    }
    print(requests.post(endpoint, data=data2).json())
    vash_token_zdes=requests.post(endpoint, data=data2).json()['data']['token']
    return vash_token_zdes

def send_message(phone_number,text,email,password, request):
    token = get_token(email,password)
    callback_url = request.build_absolute_uri(reverse('sms:get-callback'))
    if 'http://' in callback_url:
        callback_url = callback_url.replace('http://', 'https://')
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "mobile_phone": f"998{phone_number}",
        "message":text, 
        "from":"4546",
        "callback_url": callback_url  
    }
    try:
        res = requests.post(f"{url}/message/sms/send",data=data, headers=headers).json()
        SMSMessage.objects.create(phone_number=f"998{phone_number}", who_sent=request.user, type="Xabar", message=text)
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
        return 0
