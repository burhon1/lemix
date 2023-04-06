from django.utils import timezone
from getmac import get_mac_address
from user.models import CustomUser, UserDevices
from django.contrib.auth.hashers import make_password

def user_add(groups,request, is_staff=False,is_api=False):
    if is_api:
        post=request.data
    else:    
        post = request.POST
    first_name = post.get('first_name',False)
    last_name = post.get('last_name',False)
    phone = post.get('phone',False)
    password = post.get('password',False)
    birthday = post.get('birthday',False)
    gender = post.get('gender',False)
    location = post.get('location',False)
    fio = post.get('fio',False)
    educenter = request.session.get('branch_id',False)
    user = CustomUser.objects.filter(phone=phone)
    if not user.exists():
        if  phone and groups and ((first_name and last_name) or fio):
            custom_user = CustomUser(
                phone=phone,
                educenter=educenter
            )
            if birthday:
                custom_user.birthday=birthday
            if gender:
                custom_user.gender=gender
            if is_staff:     
                custom_user.is_staff=is_staff
            if location:
                custom_user.location=location
            if first_name and last_name:
                custom_user.first_name=first_name   
                custom_user.last_name=last_name 
            else:
                custom_user.first_name = fio   
            if password:
                custom_user.password = make_password(password)
            else:
                custom_user.password = make_password(phone)    
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
        if fio:
            user.last_name=fio    
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
        