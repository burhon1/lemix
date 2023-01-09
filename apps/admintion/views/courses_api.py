from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
# from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_BOOLEAN, TYPE_STRING

from admintion.serializers.courses import CourseSerializer
from admintion.models import Course
from admintion.permissions import ObjectLevelPermission


class CourseBase:
    permission_classes = [IsAuthenticated, ObjectLevelPermission]
    model = Course
    serializer_class = CourseSerializer
    queryset = Course.courses.courses()

class CoursesListAPIView(APIView):
    """
    `HEADERS`: 
        Authorization: Bearer <access_token>
    """
    queryset = None
    http_method_names = ['get', 'head', 'options']

    @swagger_auto_schema(
        responses={
            200: CourseSerializer(), 
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
        self.queryset = Course.courses.courses(**filters)
        return self.queryset


class CourseCreateAPIView(CourseBase, CreateAPIView):
    """
        Course Create API.
    """
    object_level_permissions = ['admintion.add_course']
    
    def perform_create(self, serializer):
        course = serializer.save(author=self.request.user)
        

class CourseDetailView(CourseBase, RetrieveAPIView):
    """
        Course Detail API.
    """
    object_level_permissions = ['admintion.view_course']
    
    def retrieve(self, request, *args, **kwargs):
        object = self.get_object()
        return Response(object, status=200)


class CourseUpdateView(CourseBase, UpdateAPIView):
    """
        Update API.
    """
    object_level_permissions = ['admintion.change_course']


class CourseDestroyView(CourseBase, DestroyAPIView):
    """
        Delete API.
    """
    object_level_permissions = ['admintion.delete_course']