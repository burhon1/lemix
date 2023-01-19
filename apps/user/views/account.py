from django.shortcuts import redirect


def account_view(request):
    group = request.user.groups.values_list('name',flat=True)
    if len(group)!=0:
        next = request.GET.get('next', None)
        if next:
            return redirect(next)
        if 'Admintion' in group:
            return redirect('admintion:courses')
        elif 'Teacher' in group or 'Direktor' in group:
            return redirect('admintion:dashboard')
        elif 'Student' in group:
            return redirect('student:student')   
    return redirect('user:login')        
