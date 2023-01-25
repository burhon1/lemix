from django.shortcuts import render,redirect
from django.urls import reverse
from admintion.models import Room,EduCenters
from django.db.models import Prefetch

def rooms_view(request):
    context = {}
    if request.method == "POST":
        post = request.POST
        title = post.get('title',False)
        capacity = post.get('capacity',False)
        files = request.FILES.get('files',False)
        educenter=EduCenters.objects.filter(id=request.user.educenter).first()
        if title and capacity and files:
            room = Room(
                title=title,
                capacity=capacity,
                image=files,
                educenter=educenter
            )
            room.save()
            return redirect(reverse('admintion:rooms')+f"?success={True}")
        else:
            return redirect(reverse('admintion:rooms')+f"?error=1")
    ed_id=request.user.educenter
    educenter_ids = EduCenters.objects.filter(id=ed_id).values_list('id',flat=True)|EduCenters.objects.filter(parent__id=ed_id).values_list('id',flat=True)              
    context['objs'] = Room.rooms.rooms(educenter_ids)
    return render(request,'admintion/roomslist.html',context) 