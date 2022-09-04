from django.shortcuts import render,redirect
from django.urls import reverse

from admintion.models import Room, Teacher,Course,Group,GroupsDays

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
        if title and course and status and teacher and room and trainer and days and pay_type and start_time and end_time and comments:
            course = Course.objects.filter(id=course).first()
            teacher = Teacher.objects.filter(id=teacher).first()
            room = Room.objects.filter(id=room).first()
            trainer = Teacher.objects.filter(id=trainer).first()
            days=GroupsDays.objects.filter(id__in=days)
            group = Group(
                title=title,
                comments=comments,
                course=course,
                teacher=teacher,
                trainer=trainer,
                room=room,
                pay_type=pay_type,
                status=status,
                start_time=start_time,
                end_time=end_time
            )
            group.save()
            group.days.add(*days)
            return redirect('admintion:groups')
        else:
            context['error'] = 'Malumotlar to\'liq kiritilmadi'  
            return redirect(reverse('admintion:groups')+f"?error={context['error']}")      
    context['teachers'] = Teacher.objects.filter(teacer_type=True) 
    context['trainers'] = Teacher.objects.filter(teacer_type=False)
    context['rooms'] = Room.objects.all()
    context['courses'] = Course.objects.all()
    context['groups'] = Group.groups.groups()
    print(context['groups'])
    return render(request,'admintion/groups.html',context)