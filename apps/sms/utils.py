from sms.models import SMSMessage


def get_new_dispatch_id():
    message = SMSMessage.objects.filter(dispatch_id__isnull=False).order_by('-dispatch_id').first()

    if message is None:
        dispatch_id = 1000
    else:
        dispatch_id = message.dispatch_id
    return dispatch_id+1