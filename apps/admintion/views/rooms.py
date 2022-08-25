from django.shortcuts import render,redirect
from django.urls import reverse
from admintion.models import Room

def rooms_view(request):
    context = {}
    if request.method == "POST":
        post = request.POST
        title = post.get('title',False)
        capacity = post.get('capacity',False)
        files = request.FILES.get('files',False)
        if title and capacity and files:
            room = Room(
                title=title,
                capacity=capacity,
                image=files
            )
            room.save()
            return redirect(reverse('admintion:rooms')+f"?success={True}")
        else:
            return redirect(reverse('admintion:rooms')+f"?error=1")    
    context['objs'] = Room.objects.all()
    return render(request,'admintion/roomslist.html',context) 