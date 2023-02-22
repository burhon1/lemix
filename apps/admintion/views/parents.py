from admintion.models import EduCenters, GroupStudents,Group
from django.http import JsonResponse
from admintion.utils import get_list_of_filter
from django.db.models import Q


def get_data_view(request):
    context = {}
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter_ids = EduCenters.objects.filter(qury).values_list('id',flat=True)   

    status = request.GET
    filter_keys=get_list_of_filter(status)
    course = filter_keys.get('course',False)
    group = filter_keys.get('group',False)
    if course and group:
        context['students'] = list(GroupStudents.custom_manager.student_list({'group__id':group},educenter_ids))
        # print(GroupStudents.custom_manager.student_list({'group__id':group},educenter_ids))
    elif course and not group:
        context['groups'] = list(Group.groups.group_filter_list({'course__id':filter_keys['course']},educenter_ids))
    return JsonResponse({'data':context,'status':200})