from django.shortcuts import render,redirect
from django.urls import reverse
from admintion.models import Room,EduCenters,RoomImage
from django.db.models import Prefetch
from django.db.models import Q

def rooms_view(request):
    context = {}
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter = EduCenters.objects.filter(qury)
    if request.method == "POST":
        post = request.POST
        title = post.get('title',False)
        capacity = post.get('capacity',False)
        files = request.FILES.getlist('files',False)
        educenter=educenter.first()
        if title and capacity:
            room = Room(
                title=title,
                capacity=capacity,
                educenter=educenter
            )
            room.save()
            if files:
                for fl in files:
                    room_image = RoomImage(image=fl,room=room)
                    room_image.save()
            
            return redirect(reverse('admintion:rooms')+f"?success={True}")
        else:
            return redirect(reverse('admintion:rooms')+f"?error=1")
    educenter_ids = educenter.values_list('id',flat=True)              
    context['objs'] = Room.rooms.rooms(educenter_ids)
    return render(request,'admintion/roomslist.html',context) 