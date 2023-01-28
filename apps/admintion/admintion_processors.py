from admintion.models import EduCenters

def branch_list(request):
    if request.user.is_authenticated:
        ed_id=request.user.educenter
        educenter_ids = EduCenters.educenters.educenter_id_list(ed_id)  
        branch = request.GET.get('branch',False)
        if branch:
            request.session['branch_id']=branch
        if request.session.get('branch_id',False):
            branch=request.session.get('branch_id',False)
        return {'branches':educenter_ids,'path_url':request.path,'selected_branch':int(branch)}
    return {}    