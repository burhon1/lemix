from admintion.models import EduCenters

def branch_list(request):
    if request.user.is_authenticated:
        ed_id=request.user.educenter
        educenter_ids = EduCenters.educenters.educenter_id_list(ed_id)  
        branch = request.GET.get('branch',False)
        
        if branch:
            request.session['branch_id']=branch
        elif request.session.get('branch_id',False):
            branch=request.session.get('branch_id',False)
        else:
            request.session['branch_id']=str(request.user.educenter)  
            branch=request.user.educenter 
        return {'branches':educenter_ids,'path_url':request.path,'selected_branch':int(branch)}
    return {}    

def user_groups(request):
    if request.user.is_authenticated:
        return {'groups_list':request.user.groups.values_list('name',flat=True)}
    return {}    