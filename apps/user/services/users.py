from django.utils import timezone
from getmac import get_mac_address
from user.models import CustomUser, UserDevices

def user_add(groups,request, is_staff=False):
    post = request.POST
    first_name = post.get('first_name',False)
    last_name = post.get('last_name',False)
    phone = post.get('phone',False)
    birthday = post.get('birthday',False)
    gender = post.get('gender',False)
    location = post.get('location',False)
    fio = post.get('fio',False)
    educenter = request.session.get('branch_id',False)
    user = CustomUser.objects.filter(phone=phone)
    if not user.exists():
        if  phone and birthday and gender and groups and ((first_name and last_name) or fio):
            custom_user = CustomUser.objects.create(
                phone=phone,
                birthday=birthday,
                gender=gender,
                is_staff=is_staff,
                educenter=educenter
            )
            if location:
                custom_user.location=location
            if first_name and last_name:
                custom_user.first_name=first_name   
                custom_user.last_name=last_name 
            else:
                custom_user.first_name = fio       
            
            custom_user.set_password(phone)
            custom_user.save()
            custom_user.groups.add(*groups)
            return {'status':200,'obj':custom_user}
        return {'status':1,'obj':None}   
    else:
        user = user.first()
        if first_name:
            user.first_name=first_name
        if last_name:
            user.last_name=last_name
        if phone:
            user.phone=phone
        if birthday:
            user.birthday=birthday
        if gender:
            user.gender=gender                
        user.groups.add(*groups)
        return {'status':200,'obj':user}    

def get_device_type(request):
    if request.user_agent.is_pc:
        return 'PC'
    elif request.user_agent.is_mobile:
        return 'Mobil'
    elif request.user_agent.is_tablet:
        return 'Planshet'

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_to_device_list(request):
    type_ = get_device_type(request) +'/'+ request.user_agent.os.family + ', '+ request.user_agent.browser.family
    ip = get_client_ip(request)
    device, created = UserDevices.objects.get_or_create(user=request.user, ip=ip, device=type_,mac_address=get_mac_address(ip=ip, network_request=True))
    
    if device.status == 2:
        device.status = 3
        device.save(update_fields=['status'])
        