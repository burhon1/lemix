from django import template
from student.data.choices import HOMEWORK_STATUS
register = template.Library()


def homework_status(value):
    # primary, danger, success, dark
    status_codes = {1:'dark', 2:'info', 3:'success', 4:'danger'}
    return status_codes[value]

register.filter('homework_status', homework_status)