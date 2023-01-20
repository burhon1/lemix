from django.conf import settings
from admintion.models import SmsIntegration,Messages
from admintion.services import send_sms

from sms.models import SMSAccount

def get_sms_integration(main=False):
    sms_in = SmsIntegration.objects.filter(main=main).first()
    if sms_in:
        return sms_in
    else:
        return SmsIntegration.objects.create() 
    # sms_account = SMSAccount.objects.first()
    # if sms_account is None:
    #     return None
    # elif sms_account.free_sms > 0:
    #     return settings.ESKIZ_EMAIL.values()
        

def get_bonus_smses(sms_integration):
    return sms_integration.limit

def set_used_smses(used: int):
    sms_integration = get_sms_integration()
    if sms_integration.limit> sms_integration.used:
        sms_integration.used = sms_integration.used + used
        sms_integration.limit = sms_integration.limit - used
        sms_integration.save()
    return sms_integration

def get_sms_credentials():
    """
    return `email`, `password`
    """
    sms_integration = get_sms_integration()
    if sms_integration is None:
        return None, None

    rest_bonus_sms = get_bonus_smses(sms_integration)
    if rest_bonus_sms:
        sms_integration = get_sms_integration(main=True)
        return sms_integration.email, sms_integration.password
    elif sms_integration.email and sms_integration.passsword:
        return sms_integration.email, sms_integration.password
    else:
        return None, None


def send_sms_to_user(user, text):
    email, password = get_sms_credentials()
    status = send_sms.send_message(user.phone, text, email, password)
    if status == 201:
        sms_i = get_sms_integration()
        set_used_smses(sms_i, used=1)
    else:
        print(email, password, status)

def save_sms(user,text,author,message_type=1,commit=True):
    if commit==False:
        return Messages(user=user,text=text,author=author,message_type=message_type)
    return Messages.objects.create(user=user,text=text,author=author,message_type=message_type)