from django.shortcuts import render,redirect
from django.urls import reverse

from admintion.models import Course

def courses_view(request):
    context = {}
    if request.method == "POST":
        post = request.POST
        title = post.get('title',False)
        duration = post.get('duration',False)
        lesson_duration = post.get('lesson_duration',False)
        price = post.get('price',False)
        comment = post.get('comment',False)
        
        if title and lesson_duration and duration and price and comment :
            course = Course(
                title=title,
                duration=duration,
                lesson_duration=lesson_duration,
                price=price,
                comment=comment
            )
            course.save()
            return redirect(reverse('admintion:courses')+f"?success={True}")
        else:
            return redirect(reverse('admintion:courses')+f"?error=1")    
    context['objs'] = Course.objects.all()
    return render(request,'admintion/courses_list.html',context) 