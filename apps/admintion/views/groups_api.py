from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
# from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_BOOLEAN, TYPE_STRING

from admintion.serializers.groups import GroupSerializer
from admintion.models import Group
from admintion.permissions import ObjectLevelPermission


class GroupBase:
    permission_classes = [IsAuthenticated, ObjectLevelPermission]
    model = Group
    serializer_class = GroupSerializer
    queryset = Group.groups.groups()

class GroupListAPIView(APIView):
    """
    `HEADERS`: 
        Authorization: Bearer <access_token>
    """
    queryset = None
    http_method_names = ['get', 'head', 'options']

    @swagger_auto_schema(
        responses={
            200: GroupSerializer(), 
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


class GroupCreateAPIView(GroupBase, CreateAPIView):
    """
        Group Create API.
    """
    object_level_permissions = ['admintion.add_group']
    
    def perform_create(self, serializer):
        course = serializer.save(author=self.request.user)
        

class GroupDetailView(GroupBase, RetrieveAPIView):
    """
        Group Detail API.
    """
    object_level_permissions = ['admintion.view_group']
    
    def retrieve(self, request, *args, **kwargs):
        object = Group.groups.group(id=kwargs[self.lookup_field])
        return Response(object, status=200)

class GroupUpdateView(GroupBase, UpdateAPIView):
    """
        Update API.
    """
    object_level_permissions = ['admintion.change_group']


class GroupDestroyView(GroupBase, DestroyAPIView):
    """
        Delete API.
    """
    object_level_permissions = ['admintion.delete_group']