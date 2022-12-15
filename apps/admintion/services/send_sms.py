from django.shortcuts import redirect, render,reverse
import requests

url = "http://notify.eskiz.uz/api"

def get_token(email,password):
    endpoint=f"{url}/auth/login"
    data2 = {
        "email":email,
        "password":password
    }
    vash_token_zdes=requests.post(endpoint, data=data2).json()['data']['token']
    return vash_token_zdes

def send_message(phone_number,text,email,password):
    token = get_token(email,password)
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "mobile_phone": f"998{phone_number}",
        "message":text, 
        "from":"4546",
        "callback_url":"http://0000.uz/test.php"
    }
    try:
        requests.post(f"{url}/message/sms/send",data=data, headers=headers).json()
        return 201
    except:
        return 503