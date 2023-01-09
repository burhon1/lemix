from django.urls import path
from admintion.views import courses_api, groups_api, educenters_api


urlpatterns = [
    path('courses/list/', courses_api.CoursesListAPIView.as_view(), name='api-courses-list'),
    path('courses/create/', courses_api.CourseCreateAPIView.as_view(), name='api-courses-create'),
    path('courses/detail/<int:pk>/', courses_api.CourseDetailView.as_view(), name='api-courses-detail'),
    path('courses/update/<int:pk>/', courses_api.CourseUpdateView.as_view(), name='api-courses-update'),
    path('courses/delete/<int:pk>/', courses_api.CourseDestroyView.as_view(), name='api-courses-delete'),

    path('groups/list/', groups_api.GroupListAPIView.as_view(), name='api-groups-list'),
    path('groups/create/', groups_api.GroupCreateAPIView.as_view(), name='api-groups-create'),
    path('groups/detail/<int:pk>/', groups_api.GroupDetailView.as_view(), name='api-groups-detail'),
    path('groups/update/<int:pk>/', groups_api.GroupUpdateView.as_view(), name='api-groups-update'),
    path('groups/delete/<int:pk>/', groups_api.GroupDestroyView.as_view(), name='api-groups-delete'),

    path('educenters/list/', educenters_api.EducentersListAPIView.as_view(), name='api-educenters-list'),
    path('educenters/create/', educenters_api.EducentersCreateAPIView.as_view(), name='api-educenters-create'),
    path('educenters/detail/<int:pk>/', educenters_api.EducentersDetailView.as_view(), name='api-educenters-detail'),
    path('educenters/update/<int:pk>/', educenters_api.EducentersUpdateView.as_view(), name='api-educenters-update'),
    path('educenters/delete/<int:pk>/', educenters_api.EducentersDestroyView.as_view(), name='api-educenters-delete'),
]