from django.shortcuts import render
from admintion.models import Group, EduCenters
from admintion.selectors import get_data_to_director,get_data_to_admin,get_data_to_teacher


def dashboard(request):
    context = dict()
    group = request.user.groups.first()
    
    if group.name == 'Director':
        template_name = 'admintion/dashboard_director.html'
        context['is_director'] = True
        context.update(get_data_to_director(request.user))

    if group.name == 'Admintion' or group.name == 'Manager':
        template_name = 'admintion/dashboard_director.html'
        context['is_admin'] = True
        context.update(get_data_to_admin(request.user))

    elif group.name == 'Teacher':
        template_name = 'teachers/dashboard_teacher.html'
        context['is_teacher'] = True
        context.update(get_data_to_teacher(request.user))

    return render(request, template_name, context)



def teacher_pay(request):
    context = dict()
    return render(request, 'teachers/teacher_pay.html', context)