from admintion.models import EduCenters
from django.urls import resolve


def branch_list(request):
    current_url = request.path.find('/admin/')
    if request.user.is_authenticated and  current_url==-1:
        ed_id=request.user.educenter
        educenter_ids = EduCenters.educenters.educenter_id_list(ed_id)  
        return {'branches':educenter_ids,'path_url':request.path,'selected_branch':int(request.session.get('branch_id',0))}
    return {}    

def user_groups(request):
    if request.user.is_authenticated:
        return {'groups_name_list':list(request.user.groups.values_list('name',flat=True))}
    return {}    