from django.contrib.auth.models import Group
from user.models import CustomUser

def get_user_role(user:CustomUser):
    user_group = user.groups.first()
    return user_group
    

def get_admins():
    groups = Group.objects.filter(name__in=['Manager', 'Admin', 'Direktor'])
    return CustomUser.objects.filter(groups__in=groups)

def user_exists(**kwargs):
    return CustomUser.objects.filter(**kwargs).exists()

def add_or_get_user(**kwargs):
    try:
        user, created = CustomUser.objects.get_or_create(**kwargs)
        return user
    except:
        raise Exception

def add_to_group(user:CustomUser, group_name: str, commit=True):
    try:
        group = Group.objects.get(name=group_name)
    except:
        raise Exception
    
    user.groups.add(group)
    return user
    