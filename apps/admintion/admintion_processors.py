from admintion.models import EduCenters
from django.contrib.auth.decorators import permission_required

@permission_required('admintion.view_educenters')
def branch_list(request):
    if request.user.is_authenticated:
        ed_id=request.user.educenter
        educenter_ids = EduCenters.educenters.educenter_id_list(ed_id)  
        return {'branches':educenter_ids,'path_url':request.path,'selected_branch':int(request.session.get('branch_id',0))}
    return {}    

def user_groups(request):
    if request.user.is_authenticated:
        return {'groups_list':request.user.groups.values_list('name',flat=True)}
    return {}    