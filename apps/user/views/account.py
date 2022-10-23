from django.shortcuts import redirect


def account_view(request):
    group = request.user.groups.all()
    if group.exists():
        name = group.first().name
        if name=='Student':
            return redirect('student:student')
        elif name=='Teacher':
            return redirect('education:onlin')     
    return redirect('admintion:courses')
