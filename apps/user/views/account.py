from django.shortcuts import redirect


def account_view(request):
    group = request.user.groups.all()
    if group.exists():
        name = group.first().name
        if name=='startupper':
            return redirect('user:dashboardup')
        elif name=='vc':
            return redirect('user:dashboardvc')     
    return redirect('user:dashboardup')
