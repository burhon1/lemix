from django.contrib.auth.models import Group
from user.models import CustomUser


def get_user_role(user:CustomUser):
    user_group = user.groups.first()
    return user_group
    

def get_admins():
    groups = Group.objects.filter(name__in=['Manager', 'Admin'])
    return CustomUser.objects.filter(groups__in=groups)