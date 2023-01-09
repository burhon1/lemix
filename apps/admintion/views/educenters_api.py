from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
# from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_BOOLEAN, TYPE_STRING

from admintion.serializers.educenters import EducentersSerializer
from admintion.models import EduCenters
from admintion.permissions import ObjectLevelPermission


class Educentersbase:
    permission_classes = [IsAuthenticated, ObjectLevelPermission]
    model = EduCenters
    serializer_class = EducentersSerializer
    queryset = EduCenters.educenters.educenters()

class EducentersListAPIView(APIView):
    """
    `HEADERS`: 
        Authorization: Bearer <access_token>
    """
    queryset = None
    http_method_names = ['get', 'head', 'options']

    @swagger_auto_schema(
        responses={
            200: EducentersSerializer(), 
            400: 'Bad Request',
            401: 'UnAuthorized',
            403: 'Forbidden'
        },
        # manual_parameters=[
        #     Parameter('title', IN_QUERY, 'Course title exacts', type=TYPE_STRING),
        #     Parameter('title__icontains', IN_QUERY, 'Course title contains this part of the query', type=TYPE_STRING),
        #     # Parameter('status', IN_QUERY, 'Course status', format=TYPE_BOOLEAN)
        #     ]
        )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset(**kwargs)
        return Response(self.queryset.values(), status=200)

    def get_queryset(self, **filters):
        self.queryset = Group.groups.groups(**filters)
        return self.queryset


class EducentersCreateAPIView(Educentersbase, CreateAPIView):
    """
        Educenter Create API.
    """
    object_level_permissions = ['admintion.add_educenters']
    
    def perform_create(self, serializer):
        course = serializer.save(author=self.request.user)
        

class EducentersDetailView(Educentersbase, RetrieveAPIView):
    """
        Educenters Detail API.
    """
    object_level_permissions = ['admintion.view_educenters']

    def retrieve(self, request, *args, **kwargs):
        object = self.get_object()
        return Response(object, status=200)
        
    

class EducentersUpdateView(Educentersbase, UpdateAPIView):
    """
        Update API.
    """
    object_level_permissions = ['admintion.change_educenters']


class EducentersDestroyView(Educentersbase, DestroyAPIView):
    """
        Delete API.
    """
    object_level_permissions = ['admintion.delete_educenters']