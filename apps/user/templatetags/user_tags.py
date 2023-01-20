from django import template

from user.models import CustomUser

register = template.Library()


def user_role(value):
    if type(value) is int:
        value = CustomUser.objects.filter(id=value).first()
    if value is None:
        return ''
    role = value.groups.first()
    if role:
        return role.name
    else:
        return ''


register.filter('user_role',user_role)