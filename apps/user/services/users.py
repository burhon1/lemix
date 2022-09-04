from user.models import CustomUser

def user_add(groups,post):
    first_name = post.get('first_name',False)
    last_name = post.get('last_name',False)
    phone = post.get('phone',False)
    birthday = post.get('birthday',False)
    gender = post.get('gender',False)
    location = post.get('location',False)
    if first_name and last_name and phone and birthday and gender and groups:
        custom_user = CustomUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            birthday=birthday,
            gender=gender,
            password=phone
        )
        if location:
            custom_user.location=location
        custom_user.save()
        custom_user.groups.add(*groups)
        return {'status':200,'obj':custom_user}
    return {'status':1,'obj':None}   