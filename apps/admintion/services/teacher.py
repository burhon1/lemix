from typing import Dict, List
from admintion.models import Teacher


def update_teacher(teacher: Teacher, data:Dict)-> None:
    user = teacher.user
    changed: List[str] = []
    if 'first_name' in data.keys():
        user.first_name = data.pop('first_name') or user.first_name
        changed.append('first_name')
    if 'last_name' in data.keys():
        user.last_name = data.pop('last_name') or user.last_name
        changed.append('last_name')
    if 'phone' in data.keys():
        user.phone = data.pop('phone') or user.phone
        changed.append('phone')
    if 'location' in data.keys():
        user.location = data.pop('location') or user.location
        changed.append('last_name')
    if len(changed):
        user.save(update_fields=changed)
    
    teacher.teacer_type = data.get('teacer_type', teacher.teacer_type)
    teacher.save()

    return 