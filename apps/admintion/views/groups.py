from django.shortcuts import render,redirect
from django.urls import reverse

from admintion.models import Room, Teacher

def groups_view(request):
    context = {}
    if request.method == "POST":
        post = request.POST 
        title = post.get('title',False)
        course = post.get('course',False)
        status = post.get('status',False)
        teacher = post.get('teacher',False)
        room = post.get('room',False)
        trainer = post.get('trainer',False)
        days = post.getlist('days',False)
        pay_type = post.get('pay_type',False)
        start_time = post.get('start_time',False)
        end_time = post.get('end_time',False)
        comments = post.get('comments',False)
    context['teachers'] = Teacher.objects.filter(teacer_type=True) 
    context['trainers'] = Teacher.objects.filter(teacer_type=False)
    context['rooms'] = Room.objects.all()
    print(context['teachers'])
    return render(request,'admintion/groups.html',context)