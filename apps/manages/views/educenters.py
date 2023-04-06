from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import Group
from admintion.models import EduCenters
from user.services.users import user_add

@api_view(['GET', 'POST'])
def educenters_view(request):
    if request.method == 'POST':
        data = request
        # phone = data.get('phone')
        # password = data.get('password')
        # fio = data.get('fio')
        name = data.get('name')
        groups = Group.objects.filter(name="Director")
        status,obj = user_add(groups,request,True,True).values()

        if status==200:
            educenter = EduCenters(
                name=name,
                director=obj
            )
            educenter.save()
            return Response({"message": "Got some data!", "data": educenter.name})
    educenters = EduCenters.educenters.parent_educenters()
    return Response({"educenters": list(educenters)})