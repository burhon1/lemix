from django.shortcuts import redirect


def account_view(request):
    print("in user account")
    group = request.user.groups.all()
    if group.exists():
        next = request.GET.get('next', None)
        if next:
            return redirect(next)
        name = group.first().name
        if name == 'Student':
            return redirect('student:student')
        elif name == 'Teacher' or name == 'Direktor':
            return redirect('admintion:dashboard')
        else:
            return redirect('user:login')
    return redirect('admintion:courses')
